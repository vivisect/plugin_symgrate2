import requests

LEN=18

class Symgrate2:
    """HTTP client for the Symgrate web API."""
    def __init__(self):
        self.sess = requests.session()

    def queryfn(self, bytes18):
        key = 'foo'
        nameset = self.queryfns({key: bytes18})
        if key in nameset:
            return nameset[key]

        return None

    def queryfns(self, reqdict):
        global r1
        """Queries the server for the first bytes of ASCII armored machine language."""

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        r1 = self.sess.post("http://symgrate.com/jfns", data=reqdict, headers=headers)
        
        #print r1.status, r1.reason
        # 200 OK ?
        toret=None
        if r1.status_code == 200:
            return r1.json()

        return toret

