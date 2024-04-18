"""Read and write configuration for REST APIs"""
import os
import json
import base64


class Auth():
    """Class for al functions related to BAC"""

    # Setup parameters
    def __init__(self, config_dir="config"):
        self.config_dir = config_dir

    # Base64 operations

    def encode(self, username, password):
        """Encodes credentials into base64"""

        # Convert the credentials into base64
        creds = base64.b64encode((username + ":" + password).encode('utf-8'))

        # Convert from byte to utf8
        decoded_creds = creds.decode()

        # Prefix the string with "Basic "
        return "Basic " + decoded_creds

    def decode(self, basic):
        """Decodes credentials into string"""

        # Strip the "Basic " prefix
        basic = basic.replace('Basic ', '')

        # Decode base64 into str
        creds = base64.b64decode(basic)

        decoded_creds = creds.decode()
        return decoded_creds

    # File operations

    def check_config_dir(self):
        """Checks if the config exists"""
        # If directory isn't overriden use default

        # Check if directory exists
        directory = os.path.isdir(self.config_dir)
        return directory

    def create_config_directory(self):
        """Create config directory"""
        # Try to create the directory

        if self.check_config_dir():
            print("Directory %s already exists" % self.config_dir)
            return True

        # Try to create the directory
        try:
            os.mkdir(self.config_dir)

            if self.check_config_dir():
                print("Config directory created")
                return True

        # Error creating directory
        except (IOError, PermissionError):
            print("Unable to create directory - Check permissions")

        return False

    def check_file_exists(self, config_file):
        """Check if file exists"""
        # Set path and check if it is a file
        path = self.config_dir + "/" + config_file
        file_status = os.path.isfile(path)

        return file_status

    def write_config(self, data, out_file):
        """Write config to file"""
        # Check if config dir exists
        if not self.check_config_dir():
            print("Config directory doesn't exist")
            # Create dir
            if not self.create_config_directory():
                os.sys.exit()

        # Write to file
        try:
            print("Writing to %s" % (self.config_dir + '/' + out_file))
            with open(self.config_dir + '/' + out_file, 'w') as outfile:
                json.dump(data, outfile)

        # Error writing to file
        except (IOError, PermissionError):
            print("Unable to write to config file %s, check permissions" %
                  (self.config_dir + '/' + out_file))
            return False

        # File was written successfully
        file_check = self.check_file_exists(out_file)
        return file_check

    def read_config(self, file):
        """Open file and return contents as dict"""
        # Try to open the file
        try:
            with open(self.config_dir + '/' + file) as file_in:
                try:
                    data = json.load(file_in)
                except json.decoder.JSONDecodeError:
                    return False
                return data

        # Error opening file
        except (PermissionError, IOError, FileNotFoundError):
            return False

    def verify_config(self, file, key, value):
        """Verify if a key is in a file and check value"""
        # Get the file contents
        contents = self.read_config(file)
        try:
            # Verify th ekey contents
            return contents[key] == value
        except (TypeError, KeyError):
            return False

    def create_config(self, filename, config):
        """Write the config to a file"""

        # Create dir and file
        if self.create_config_directory():
            if self.write_config(config, filename):
                return True
        return False

    def ask(self, message):
        """Ask a question and return the response"""
        # Get user input
        config = input(message + ": ")
        return config

    def basic_config_generate(self, url: str, basic_auth: str):
        """Template for a basic set of settings"""
        # Create basic data structure
        config = {}
        config['url'] = url
        config['authorization'] = basic_auth

        return config

    def basic_config(self, url: str, username: str, password: str):
        """Takes basic input and writes config to config.json"""
        config = self.basic_config_generate(url,
                                            self.encode(username, password))
        return self.write_config(config, "config.json")
