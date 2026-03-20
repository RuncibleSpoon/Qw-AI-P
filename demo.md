

Scan:
```
endorctl scan -n henrik-report.sast-ai-demo --sast --dependencies
```

Get callgraph with source code
```
endorctl api get -r CallGraphData -n henrik-report.sast-ai-demo --bypass-host-check --header "x-endor-callgraph-encoding: any" --uuid 67ebfad98ee24cd6a1697e7e
```

Get LinterResults for sources and sinks:
```
endorctl api list --bypass-host-check -r LinterResult -n henrik-report.sast-ai-demo --filter "meta.name==python-sources"
endorctl api list --bypass-host-check -r LinterResult -n henrik-report.sast-ai-demo --filter "meta.name==python-sinks-cwe-79"
endorctl api list --bypass-host-check -r LinterResult -n henrik-report.sast-ai-demo --filter "meta.name==python-sinks-cwe-89"
```