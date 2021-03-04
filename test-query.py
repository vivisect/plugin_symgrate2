#!/usr/bin/env python3

from Symgrate2 import Symgrate2

fn_samples=["0a460346024908681946fff7b9bf00bfc400"];

symg = Symgrate2()

for sample in fn_samples:
    res = symg.queryfn(sample);
    if res != None:
        print("name: %-10s filename: %s (%s)"%(res['Name'], res['Filename'], sample));

fns_samples = {
        'foo': '0a460346024908681946fff7b9bf00bfc400',
        'bar': '012020e000c0a0e1030012e33200001a0300',
        'baz': '02780b78012a28bf9a42f5d16de9044540ea',
        }
res = symg.queryfns(fns_samples)
for k, v in res.items():
    print("%s:  name: %-10s filename: %s"%(k, v['Name'], v['Filename']));

