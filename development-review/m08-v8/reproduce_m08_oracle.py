import argparse,hashlib,itertools,json,pathlib
parser=argparse.ArgumentParser(description='Reproduce the unadopted M08 finite routing oracle; never import the model.')
parser.add_argument('--output',type=pathlib.Path,required=True)
args=parser.parse_args()
# Independent oracle records all joint outcomes, without calling the review model.
rows=[]
for b,c,r,f,s in itertools.product(('MATCH','MISMATCH','MISSING','INVALID','CONTRADICTORY'),('MATCH','MISMATCH','MISSING','UNKNOWN'),('EQUAL','DIFFERENT','UNKNOWN','CONTRADICTORY'),('CURRENT','STALE','UNKNOWN'),('SATISFIED','BLOCKED','UNRESOLVED')):
    classification='SATISFIED'
    if b in ('MISMATCH','INVALID','CONTRADICTORY') or c=='MISMATCH' or r=='CONTRADICTORY':classification='BLOCKED'
    elif b=='MISSING' or c in ('MISSING','UNKNOWN') or r=='UNKNOWN':classification='UNRESOLVED'
    decision=('denial_preserves_atlas',classification,'PROPOSED' if classification=='BLOCKED' else 'STALE','CLOSED')
    if classification=='SATISFIED':
        if r=='DIFFERENT':decision=('denial_with_intervening_drift','SATISFIED','STALE','CLOSED')
        elif f=='STALE':decision=('denial_with_insufficient_freshness','SATISFIED','STALE','CLOSED')
        elif f=='UNKNOWN':decision=('denial_with_insufficient_freshness','UNRESOLVED','STALE','CLOSED')
        else:decision=('denial_preserves_atlas','SATISFIED','DERIVED','ALLOWED' if s=='SATISFIED' else 'CLOSED')
    rows.append({'components':[b,c,r,f,s],'expected':{'comparison_classification':classification,'route_event':decision[0],'route_outcome':decision[1],'target_state':decision[2],'ordinary_access':decision[3]}})
table=json.dumps({'scope':'UNADOPTED_INDEPENDENT_JOINT_ORACLE','rows':rows},indent=2,sort_keys=True).encode()

pin='23de4796fa572bae329ce1de1117418d50fe9e01b3485ec3bff23f234f507ade'
actual=hashlib.sha256(table).hexdigest()
if actual!=pin:raise SystemExit('ORACLE_REPRODUCTION_DIGEST_MISMATCH')
with args.output.open('xb') as stream:stream.write(table)
print(json.dumps(dict(rows=len(rows),bytes=len(table),sha256=actual,scope='UNADOPTED_PURE_ORACLE_REPRODUCTION')))
