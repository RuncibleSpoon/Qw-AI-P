# Semgrep Results

## Run

You need our Endor Semgrep rules: 

`git clone https://github.com/endorlabs/semgrep-rules/`

Then you can run semgrep with those rules directly command line:
`semgrep scan --sarif-output semgrep-results.sarif --config /Users/lucacompagna/git/endor/sast-lab/endor_semgrep_rules/rules .`

Note: Alternatively we could use endorctl and make a SAST scan.

## Results - raw
Here the results when running with semgrep command line:

```
(.venv) lucacompagna@Lucas-MacBook-Pro QwietAI-python-demo-ext % semgrep scan --sarif-output semgrep-results.sarif --config /Users/lucacompagna/git/endor/sast-lab/endor_semgrep_rules/rules . 

┌──── ○○○ ────┐
│ Semgrep CLI │
└─────────────┘

                                                                                                                        
Scanning 1211 files (only git-tracked) with 633 Code rules:
            
  CODE RULES
                                                                                                                        
  Language      Rules   Files          Origin   Rules                                                                   
 ─────────────────────────────        ────────────────                                                                  
  <multilang>       2      30          Custom     633                                                                   
  python           74       8                                                                                           
                                                                                                                        
                    
  SUPPLY CHAIN RULES
                                                       
  💎 Run `semgrep ci` to find dependency
     vulnerabilities and advanced cross-file findings. 
                                                       
          
  PROGRESS
   
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00                                                                                                                        
                    
                    
┌──────────────────┐
│ 11 Code Findings │
└──────────────────┘
                                           
    flask_webgoat/actions.py
   ❯❯❱ Users.lucacompagna.git.endor.sast-lab.endor_semgrep_rules.rules.3p.gitlab.python.exec.python_exec_rule-
       subprocess-popen-shell-true                                                                            
          Problem: Found `subprocess` function `run` with `shell=True`. This is dangerous because this call
          will spawn the command using a shell process. Doing so propagates current shell settings and     
          variables, which makes it much easier for a malicious actor to execute commands.                 
                                                                                                           
          Solution: Use `shell=False` instead.                                                             
                                                                                                           
           44┆ res = subprocess.run(
           45┆     ["ps aux | grep " + name + " | awk '{print $11}'"],
           46┆     shell=True,
           47┆     capture_output=True,
           48┆ )
   
    ❯❱ Users.lucacompagna.git.endor.sast-                                                               
       lab.endor_semgrep_rules.rules.3p.gitlab.python.deserialization.python_deserialization_rule-pickle
          Problem: The application was found using `pickle` which is vulnerable to deserialization attacks.   
          Deserialization attacks exploit the process of reading serialized data and turning it back into an  
          object. By constructing malicious objects and serializing them, an adversary may attempt to: -      
          Inject code that is executed upon object construction, which occurs during the deserialization      
          process - Exploit mass assignment by including fields that are not normally a part of the serialized
          data but are read in during deserialization                                                         
                                                                                                              
          Solution: Consider safer alternatives such as serializing data in the JSON format. Ensure any format
          chosen allows the application to specify exactly which object types are allowed to be deserialized. 
          To protect against mass assignment, only allow deserialization of the specific fields that are      
          required. If this is not easily done, consider creating an intermediary type that can be serialized 
          with only the necessary fields exposed.                                                             
                                                                                                              
          Example JSON deserializer using an intermediary type that is validated against a schema to ensure it
          is safe from mass assignment: ``` import jsonschema                                                 
                                                                                                              
          # Create a schema to validate our user-supplied input against # an intermediary object              
          intermediary_schema = {     "type": "object",     "properties": {         "name": {"type": "string"}
          },     "required": ["name"],     # Protect against random properties being added to the object      
          "additionalProperties": False, } # If a user attempted to add "'is_admin': True" it would cause a   
          validation error intermediary_object = {'name': 'test user'}                                        
                                                                                                              
          try:     # Validate the user supplied intermediary object against our schema                        
          jsonschema.validate(instance=intermediary_object, schema=intermediary_schema)     user_object = {   
          'user': {             # Assign the deserialized data from intermediary object             'name':   
          intermediary_object['name'],             # Add in protected data in object definition (or set it    
          from a class constructor)             'is_admin': False,         }     }     # Work with the        
          user_object except jsonschema.exceptions.ValidationError as ex:     # Gracefully handle validation  
          errors     # ... ```                                                                                
                                                                                                              
          For more details on deserialization attacks in general, see OWASP's guide: -                        
          https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html                     
                                                                                                              
           61┆ deserialized = pickle.loads(data)
   
    ❯❱ Users.lucacompagna.git.endor.sast-lab.endor_semgrep_rules.rules.endor.vuln.python.python_pickle_deserialization
          Problem: The application was found using `pickle` which is vulnerable to deserialization attacks.   
          Deserialization attacks exploit the process of reading serialized data and turning it back into an  
          object. By constructing malicious objects and serializing them, an adversary may attempt to: -      
          Inject code that is executed upon object construction, which occurs during the deserialization      
          process - Exploit mass assignment by including fields that are not normally a part of the serialized
          data but are read in during deserialization                                                         
                                                                                                              
          Solution: Consider safer alternatives such as serializing data in the JSON format. Ensure any format
          chosen allows the application to specify exactly which object types are allowed to be deserialized. 
          To protect against mass assignment, only allow deserialization of the specific fields that are      
          required. If this is not easily done, consider creating an intermediary type that can be serialized 
          with only the necessary fields exposed.                                                             
                                                                                                              
          Example JSON deserializer using an intermediary type that is validated against a schema to ensure it
          is safe from mass assignment: ``` import jsonschema                                                 
                                                                                                              
          # Create a schema to validate our user-supplied input against # an intermediary object              
          intermediary_schema = {     "type": "object",     "properties": {         "name": {"type": "string"}
          },     "required": ["name"],     # Protect against random properties being added to the object      
          "additionalProperties": False, } # If a user attempted to add "'is_admin': True" it would cause a   
          validation error intermediary_object = {'name': 'test user'}                                        
                                                                                                              
          try:     # Validate the user supplied intermediary object against our schema                        
          jsonschema.validate(instance=intermediary_object, schema=intermediary_schema)     user_object = {   
          'user': {             # Assign the deserialized data from intermediary object             'name':   
          intermediary_object['name'],             # Add in protected data in object definition (or set it    
          from a class constructor)             'is_admin': False,         }     }     # Work with the        
          user_object except jsonschema.exceptions.ValidationError as ex:     # Gracefully handle validation  
          errors     # ... ```                                                                                
                                                                                                              
          For more details on deserialization attacks in general, see OWASP's guide: -                        
          https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html                     
                                                                                                              
           61┆ deserialized = pickle.loads(data)
                                        
    flask_webgoat/auth.py
    ❯❱ Users.lucacompagna.git.endor.sast-lab.endor_semgrep_rules.rules.endor.vuln.python.python-flask-open-redirect
          Problem: The application uses user-controlled input to determine the destination URL in redirection 
          logic, potentially leading to an open redirect vulnerability. This issue allows attackers to        
          redirect users to malicious websites, enabling phishing attacks or other social engineering         
          exploits.                                                                                           
                                                                                                              
          In Flask applications, passing untrusted input from sources like query parameters (e.g.,            
          `request.args.get`) directly to `redirect()` functions without validation or sanitization is        
          particularly risky.                                                                                 
                                                                                                              
          Key risks of open redirects include: * Phishing attacks: Attackers can redirect users to malicious  
          sites that appear legitimate. * Loss of user trust: Victims may associate the malicious activity    
          with your application.                                                                              
                                                                                                              
          Solution: To remediate this issue, validate the input used in redirection logic by implementing a   
          whitelist of trusted URLs or domains. Reject any URLs that are not explicitly trusted.              
                                                                                                              
          Example using a whitelist in Python Flask: ``` SAFE_URLS = ['https://trusted.com', 'https://another-
          trusted.com']                                                                                       
                                                                                                              
          @app.route('/redirect') def safe_redirect():     target = request.args.get('target')     if target  
          in SAFE_URLS:         return redirect(target)     else:         return abort(400) ```               
                                                                                                              
          This example ensures that only URLs listed in `SAFE_URLS` are allowed, and any untrusted input      
          results in a `400 Bad Request`.                                                                     
                                                                                                              
          For more information on open redirect vulnerabilities, see: - OWASP:                                
          https://cheatsheetseries.owasp.org/cheatsheets/Open_Redirect_Cheat_Sheet.html                       
                                                                                                              
           49┆ return redirect(url)
            ⋮┆----------------------------------------
           91┆ return redirect(url)
                                                  
    flask_webgoat/user_resources.py
     ❱ Users.lucacompagna.git.endor.sast-lab.endor_semgrep_rules.rules.3p.gitlab.python.random.python_random_rule-
       random                                                                                                     
          Problem: Depending on the context, generating weak random numbers may expose cryptographic         
          functions, which rely on these numbers, to be exploitable.                                         
                                                                                                             
          Solution: When generating numbers for sensitive values such as tokens, nonces, and cryptographic   
          keys, it is recommended that the `secrets` module be used instead.                                 
                                                                                                             
          Example using the secrets module: ``` import secrets # Generate a secure random 64 byte array      
          random_bytes = secrets.token_bytes(64) print(random_bytes) # Generate a secure random 64 byte array
          as a hex string random_bytes_hex = secrets.token_hex(64) # Generate a secure random 64 byte array  
          base64 encoded for use in URLs random_string = secrets.token_urlsafe(64) ```                       
                                                                                                             
          For more information on the `secrets` module see: - https://docs.python.org/3/library/secrets.html 
                                                                                                             
           45┆ random_suffix = random.randint(1000, 9999)
                                         
    flask_webgoat/users.py
    ❯❱ Users.lucacompagna.git.endor.sast-lab.endor_semgrep_rules.rules.endor.vuln.python.python-flask-xss
          Potential Cross-Site Scripting (XSS) vulnerability detected in Python Flask application. XSS occurs 
          when unsanitized user input is included in web pages, allowing attackers to inject malicious        
          scripts. This can lead to session hijacking, defacement, or redirection to malicious sites. The rule
          identifies sources of unsanitized input, such as request parameters and headers, and tracks their   
          flow to sinks like template rendering and response manipulation functions, which can result in XSS  
          if not properly sanitized.                                                                          
                                                                                                              
           44┆ print(f"Attempting to create user: {username} with access level: {access_level}")
            ⋮┆----------------------------------------
           46┆ print(f"Result of query_db: {result}")
            ⋮┆----------------------------------------
           51┆ print(f"Verification query result: {user}")
            ⋮┆----------------------------------------
           89┆ print(f"Attempting to delete user with ID: {id}")
            ⋮┆----------------------------------------
           95┆ print(f"Verification result (None means deletion successful): {user}")
```

## Results - inspection and demo candidates

Semgrep reports 11 code findings.

- [x] subprocess shell (rule: `python_exec_rule-
       subprocess-popen-shell-true`): no much we can do, apart e.g., disabling the corresponding rule once the user tells us to do so in the AI prompt console of Endor platform
- [ ] pickle deserialization (rule: ``): ignore for the moment
- [x] open redirect - dataflow (rule: `python-flask-open-redirect`)
    - two results are reported for file `./flask_webgoat/auth.py`. 
    - One is a false positive (line 91), the other is a true positive. 
    - **Demo candidate (reduce FPs)**: our dataflow AI-based approach should report the TP but not the FP. TO BE CHECKED
- [x] Random number generator (rule: `python_random_rule-random`)
    - **Demo candidate (reduce FPs)**: our AI-based approach (no dataflow here) on top of semgrep result should be able to analyse the context and decide that this is a FP 
- [x] XSS - dataflow (rule: `python-flask-xss`)
    - 5 results are reported about the `print`: these are all FPs as print is not going into the response
    - **Demo candidate (reduce FPs)**: our dataflow AI-based approach should be able to analyse this correctly 

**Demo candidate (reduce FNs)** Our semgrep rules are missing a number of dataflow related TPs. Hopefully our dataflow AI-based approach should score better  