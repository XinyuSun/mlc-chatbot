import os
import re
import platform
from subprocess import Popen, PIPE


class ChatBot(object):
    def __init__(self, dist_dir="", cli_dir="", verbose=False):
        """
        Initialize the ChatBot object.

        :param dist_dir: str, optional
            The path to the dist directory of mlc llm. Defaults to the current directory.
        :param cli_dir: str, optional
            The path to the CLI executable directory. Defaults to PATH.
        :param verbose: bool, optional
            If True, the ChatBot will print more detailed information for debugging purposes. 
            Defaults to False.
        """
        self.verbose = verbose
        self.prefix = "USER: ASSISTANT: "

        dist_dir = os.path.abspath(os.path.dirname(dist_dir))
        cli_dir = os.path.abspath(os.path.dirname(cli_dir))
        os_name = platform.system()
        if os_name == "Windows":
            cmd = os.path.join(cli_dir, "mlc_chat_cli.exe")
        elif os_name in ["Darwin", "Linux"]:
            cmd = os.path.join(cli_dir, "mlc_chat_cli")
        
        self._verbose_print(cmd)
        self._verbose_print(dist_dir)

        self.process = Popen(
            [cmd],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            cwd=dist_dir
        )

        output = self.process.stdout.readline().strip()
        while output:
            self._verbose_print(output)
            output = self.process.stdout.readline().strip()
    
    def __exit__(self):
        self._verbose_print("exiting mlc chat...")
        self.terminate()
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait(timeout=1)

    def _verbose_print(self, text):
        if self.verbose:
            print(text)

    def _crop(self, text):
        if text.startswith("USER"):
            text = text[len("USER: "):]
        if text.startswith("ASSISTANT"):
            text = text[len("ASSISTANT: "):]
        return text

    def _write(self, text):
        self.process.stdin.write(text + "\n")
        self.process.stdin.flush()
        return self._crop(self.process.stdout.readline().strip())

    def send(self, text):
        return self._write(text)

    def terminate(self):
        self._verbose_print(self._write('/exit'))

    def reset(self):
        self._verbose_print(self._write('/reset'))
    
    def status(self):
        _stats = self._write('/stats')
        encode_v = re.compile(r"encode:\s+(\d+(\.\d+)?)\s+tok/s").search(_stats)
        encode_v = float(encode_v.group(1)) if encode_v else 'nan'
        decode_v = re.compile(r"decode:\s+(\d+(\.\d+)?)\s+tok/s").search(_stats)
        decode_v = float(decode_v.group(1)) if decode_v else 'nan'
        self._verbose_print(_stats)
        return encode_v, decode_v