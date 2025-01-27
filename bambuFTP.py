import ftplib
import ssl
import os



class ImplicitFTP_TLS(ftplib.FTP_TLS):
    """FTP_TLS subclass that automatically wraps sockets in SSL to support implicit FTPS."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        """Return the socket."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """When modifying the socket, ensure that it is ssl wrapped."""
        if value is not None and not isinstance(value, ssl.SSLSocket):
            value = self.context.wrap_socket(value)
        self._sock = value

class BambuPrinterFTP:
    ip = "127.0.0.1"
    passwd = ""
    user = ""
    ftp_client = ImplicitFTP_TLS()

    def __init__(self, device_ip, access_code, user = "bblp"):
        self.ip = device_ip
        self.passwd = access_code
        self.user = user

    def connect(self):
        self.ftp_client.connect(host = self.ip, port = 990, timeout = 20)
        self.ftp_client.login(user = self.user, passwd = self.passwd)
        self.ftp_client.prot_p()

    def get_file(self, filename, path = './temp/temp.3mf'):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as fp:
            self.ftp_client.retrbinary(f'RETR {filename}', fp.write)
        return

    def get_last_file():
        return

    def close_connection(self):
        self.ftp_client.quit()
        return
    
    