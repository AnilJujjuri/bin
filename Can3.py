const modbus = require('modbus-tcp-ip')

let twin = null;
let myedgeClient = null;
let myMessage = null;
async function collect(edgeClient, Message) {
    // for (let index = 0; index < connection.length; index++) {
    while (true) {
        try {
            console.log("Running")
            let connection = await getConnection();
            connection = connection.devices;
            console.log(connection)
            if (connection) {
                for (const key in connection) {
                    if (connection.hasOwnProperty(key)) {
                        const element = connection[key];

                        let telemetry = { "thingId": element.thingId, "deviceId": element.id, "message_type": "telemetry", "data": {} };
                        try {
                            // step 1 : connect to
                            let device = modbus(element.connection.ipAddress, element.connection.port, element.connection.slaveId ? element.connection.slaveId : 1);
                            // modbus.on('error', function (err) {
                            //     console.log("Captured the close event")
                            // });
                            console.log("connected !");

                            for (const key in element.signals) {
                                if (element.signals.hasOwnProperty(key)) {
                                    const signal = element.signals[key];
                                    console.log(signal.name)
                                    let value = await device.read(GetAddress(signal.address, signal.length));
                                    console.log(value)
                                    telemetry.data[signal.name] = value;
                                }
                            }

                            telemetry.ts = (Date.now() / 1000).toFixed(0);
                            console.log(telemetry);

                            try {
                                // var message = telemetry.getBytes().toString('utf8');
                                if (telemetry) {
                                    var outputMsg = new Message(JSON.stringify(telemetry));
                                    edgeClient.sendOutputEvent('modbustcpTelemetry', outputMsg, printResultFor('Sending received message'));
                                }
                            } catch (error) {
                                console.log("Failed to send data to cloud -" + error);
                            }
                            // disconnecting
                            device = null;
                            console.log("done !");
                        } catch (err) {
                            console.log("An error has occured : ", err);
                        }
                        await timeout(element.interval);
                    }
                }
            }
        } catch (error) {
            console.log("Error in communication/processing " + err)
        }
        await timeout(100);
    }
}
// add this handler before emitting any events
process.on('uncaughtException', function (err) {
    console.log('Starting Data Aquistion Task');
    collect(myedgeClient, myMessage);
    console.log('UNCAUGHT EXCEPTION - keeping process alive:', err); // err.message is "foobar"
});

async function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function setConnection(twinObj, edgeClient, Message) {
    console.log(twin)
    myedgeClient = edgeClient;
    myMessage = Message;
    if (twin === null) {
        twin = twinObj;//.properties.desired;
        setTimeout(() => {
            console.log('Starting Data Aquistion Task');
            collect(edgeClient, Message);
        }, 1000);
    } else {
        twin = twinObj;//.properties.desired;
    }
    console.log("Updated twin")
    console.log(twinObj)
    console.log(twin)
}

async function getConnection() {
    return twin;
}

// Helper function to print results in the console
function printResultFor(op) {
    return function printResult(err, res) {
        if (err) {
            console.log(op + ' error: ' + err.toString());
        }
        if (res) {
            console.log(op + ' status: ' + res.constructor.name);
        }
    };
}

// FOR DEBUG PURPOSE ONLY
// let obj = {
//     'devices': {
//         "1001": {
//             id: '1001',
//             type: 'modbus-tcp',
//             thingId: '2001',
//             interval: '10000',
//             connection: {
//                 ipAddress: '52.149.144.189',
//                 port: '502',
//                 slaveId: '1'
//             },
//             signals: {
//                 "temperature": {
//                     name: "temperature",
//                     address: '30001',
//                     length: '1',
//                     unitId: '1',
//                     interval: '1000'
//                 },
//                 "humidity": {
//                     name: "humidity",
//                     address: '30002',
//                     length: '1',
//                     unitId: '2',
//                     interval: '1000'
//                 }
//             }
//         }
//     }
// }

// setConnection(obj, null, null);
function GetAddress(address, length) {
    let fc = address.split('')[0];
    let temp = address.slice(1);
    let response = '';
    switch (fc) {
        case '1':
            response = 'c' + temp;
            break;
            break;
        case '2':
            response = 'i' + temp;
        case '3':
            response = 'hr' + temp;
            break;
        case '4':
            response = 'ir' + temp;
            break;
        default:
        //TBD
    }
    if (Number(length) > 1) {
        response = response + '-' + (Number(temp) + Number(length))
    }
    return response;
}

module.exports = { setConnection }

