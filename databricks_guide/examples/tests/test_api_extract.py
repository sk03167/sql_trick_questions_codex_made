import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from email.message import Message
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'templates'))
from api_extract import extract_pages,fetch_page
class ApiTests(unittest.TestCase):
    def directory(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup)
        return Path(t.name)/'run'
    def test_two_pages(self):
        pages={None:{'items':[{'id':1}],'next_cursor':'b'},'b':{'items':[{'id':2}],'next_cursor':None}}
        p=self.directory();m=extract_pages(pages.__getitem__,p)
        self.assertEqual(m['records'],2);self.assertTrue((p/'manifest.json').exists())
    def test_empty_page_still_advances(self):
        pages={None:{'items':[],'next_cursor':'b'},'b':{'items':[{'id':2}]}}
        self.assertEqual(extract_pages(pages.__getitem__,self.directory())['records'],1)
    def test_cursor_loop_no_manifest(self):
        p=self.directory()
        with self.assertRaises(ValueError): extract_pages(lambda c:{'items':[],'next_cursor':'b'},p)
        self.assertFalse((p/'manifest.json').exists())
    def test_page_limit_no_manifest(self):
        p=self.directory()
        with self.assertRaises(RuntimeError): extract_pages(lambda c:{'items':[],'next_cursor':'b'},p,max_pages=1)
        self.assertFalse((p/'manifest.json').exists())
    def test_failure_no_manifest(self):
        p=self.directory()
        def fail(c): raise TimeoutError()
        with self.assertRaises(TimeoutError):extract_pages(fail,p)
        self.assertFalse((p/'manifest.json').exists())
    def test_wrong_contract(self):
        with self.assertRaises(ValueError):extract_pages(lambda c:{'data':[]},self.directory())
    def test_existing_folder_refused(self):
        p=self.directory();p.mkdir()
        with self.assertRaises(FileExistsError):extract_pages(lambda c:{'items':[]},p)
    def test_429_bounded_retries(self):
        h=Message();h['Retry-After']='2'
        e=HTTPError('https://api.example.invalid',429,'rate limited',h,None)
        waits=[]
        with patch('api_extract.urlopen',side_effect=e) as opener:
            with self.assertRaises(HTTPError):fetch_page('https://api.example.invalid/v1/orders','test',None,retries=2,sleep=waits.append)
        self.assertEqual(opener.call_count,3);self.assertEqual(waits,[2.0,2.0])
    def test_401_not_retried(self):
        e=HTTPError('https://api.example.invalid',401,'unauthorized',Message(),None)
        with patch('api_extract.urlopen',side_effect=e) as opener:
            with self.assertRaises(HTTPError):fetch_page('https://api.example.invalid/v1/orders','test',None,sleep=lambda _:None)
        self.assertEqual(opener.call_count,1)
if __name__=='__main__':unittest.main()
