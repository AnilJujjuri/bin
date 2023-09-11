import unittest
import io
import sys
import time
from your_module_name import create_client_with_retry

class TestCreateClientWithRetry(unittest.TestCase):
    def test_successful_connection(self):
        # Save the original sys.stdout for later comparison
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()

        # Mock a successful client creation
        def mock_create_client(*args, **kwargs):
            return 'mocked_client'

        with unittest.mock.patch('azure.iot.device.IoTHubModuleClient.create_from_connection_string', side_effect=mock_create_client):
            # Call the function with max_retries=3, retry_delay=1
            client = create_client_with_retry(max_retries=3, retry_delay=1)

        # Restore sys.stdout
        sys.stdout = original_stdout

        # Assert that the client was created and no retries were needed
        self.assertEqual(client, 'mocked_client')
        self.assertIn("Client connected successfully", sys.stdout.getvalue())

    def test_failed_connection_with_retry(self):
        # Save the original sys.stdout for later comparison
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()

        # Mock exceptions on the first two attempts
        def mock_create_client(*args, **kwargs):
            if mock_create_client.call_count < 3:
                raise Exception(f'Attempt {mock_create_client.call_count}')
            return 'mocked_client'

        with unittest.mock.patch('azure.iot.device.IoTHubModuleClient.create_from_connection_string', side_effect=mock_create_client):
            # Call the function with max_retries=3, retry_delay=1
            client = create_client_with_retry(max_retries=3, retry_delay=1)

        # Restore sys.stdout
        sys.stdout = original_stdout

        # Assert that the client was created after two retries
        self.assertEqual(client, 'mocked_client')
        self.assertIn("Client connected successfully after 2 retries", sys.stdout.getvalue())

    def test_failed_connection_without_retry(self):
        # Save the original sys.stdout for later comparison
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()

        # Mock exceptions on all attempts
        def mock_create_client(*args, **kwargs):
            raise Exception(f'Attempt {mock_create_client.call_count}')

        with unittest.mock.patch('azure.iot.device.IoTHubModuleClient.create_from_connection_string', side_effect=mock_create_client):
            # Call the function with max_retries=3, retry_delay=1
            client = create_client_with_retry(max_retries=3, retry_delay=1)

        # Restore sys.stdout
        sys.stdout = original_stdout

        # Assert that the client is None because retries exceeded the limit
        self.assertIsNone(client)
        self.assertIn("Failed to connect after 3 retries", sys.stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
