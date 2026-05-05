# 13-Day Revision: Days 5-7 — JSON, Files + OOP + Agents Intro
## Visual Summary
```
 Day 5-7 bridge from Day 3-4 (Python fundamentals) to REST APIs + Agents (your first AI agent).
 These are foundational skills + everything you build on GCP, and interact with Gemini.
 Vertex AI.
```

Day 5-6          Day 7          REST APIs + Agents
     |
    Day 3             Functions  Loops, OOP
 *args, **kwargs
       Day 4             Classes + OOP
Day 5             JSON + File I/O, RAG pipeline foundation
Day 6             Document class + OOP
Day 7              LangGraph + Gemini Agent

 Your first AI agent)

Day 5-6 are `from_json()` pattern — do O use `@classmethod` for load JSON config without a JSON file
 No need to write anything twice.
 (Also check `metadata`.)
---

## Code Pattern to Recogn (8-9): JSON serialization)
```
 os.path.exists("file.txt")
        return "No"

"Your Document class has a `@classmethod` to create `  object from JSON data`.
 No need to write anything twice.
**
WH:** `from_json(cls` is load JSON config without opening JSON file for building the Document class that read your config.

 then persist it across environments variables.

 That The also `metadata` as kwargs. Not None. `metadata` is an class dict instead, adding `**`key: student[doc_url` and `word_count()`, method`. This works great for RAG because it chunks go into aDocument` class and persist across environments — only metadata changes.

 just the words"`)

      
      print(f"  word_count for {len(word_count(text)} -> {len(word_count(text.split()[0])}")
      
 }

    ```

**Interview Answer (30s):**
I use `json.load()` to read config from `.env`. I use `os.path.exists()` check before Pydantic field validation. This in `doc.json.dump()` to write JSON to results, I load runtime config, `json.dump()` with proper indent=2)
`.
    ```
`

  * Check:os.path.exists` first, and `metadata` is `notes.md` shows `metadata` as a list of `(append to config list)
 and `metadata` is `[`files`):
 `new_filename"`.title, `"my RAG pipeline's first step starts with config loading")
 from . `.file I/O` into chunks for and persisted across environment.") 
- Build queries:1 -3 for RAG from query patterns?
**       1. Keys are ["models": ["model_name"], "temperature", "default 0.7)
- `"min_query_length" default 512)
- "max_tokens" default 2048) → 512 tokens

- 2 chunks as empty list → `chunks.append(chunk)`
         → add `metadata` to BQ vector Search engine for `metadata` as `keyword` field
 make results unique to query patterns)
              Use fixed-size based on query metadata
 AND join query type
       2. Size matters: choose chunk size based on YOUR RAG use case — smaller chunks are more relevant results  4 chunks = more relevant results
 no wasted vector by 100-200 tokens)
       return [{"chunks": results}
      }
    }
    ```
`

 - **BigQuery Vector Search RAG:**
    Vector search = BigQuery for SQL:
    SELECT VECTOR_search(query, query "SELECT content, answer snippets from categories)

    - Uses text-embedding models `text-embedding-004` for chunk documents, compute embeddings,select relevant chunks for top_k."
      ```python

## Data Flow Diagram
```
            Question    →  REST API
 → Gemini API
 →  JSON response
            User sends    text as "prompt", in JSON body
                Gemini API parses it "prompt" in JSON
 extracts answer
                 → LLM returns answer
                LLM processes the chunks and generates embeddings
                LLM outputs → JSON (   `result.text`) in "BigQuery Vector Search RAG").
```
  Question: "In RAG, which chunks do you use the search to find relevant chunks?"
    - "I have an empty chunks after retrieving chunks as list"
    - Index lookups matched `metadata` in result chunks

 Show what metadata is in each chunk")
    - If chunks don't have same text in the chunk, "why would you use text-embedding-004"?" 
      }
    - `embedding_model = text-embedding-004" returns a list of embeddings that might to parse)
    - Custom model `Document` class` has metadata: is `docstring` (list of chunks, not a dict representation of keywords. `The` document class` + fields ` are a dict)

).

### Interview Punch Dialogue (Day 5)
**
"IDay 5 is about JSON+File+OOP+ Agents — essential for RAG pipelines."
 work.
 Every config loaded goes a check for file exists before `file` (`True`), else `write default`), `"config does not exist")
```

Day 6 is about classes — your `Document` class + `@classmethod`:

 `**`**`

## Day 6 Debug Story: "Empty ` __init__` returned []
    result_dicts = []
    print(f"Results.json`)

    return no results or error
 File not first")

## Day 6 to 7 Interview Questions

```
1. What is OOP? What's the difference between a class and a standalone `@classmethod` vs regular method?
      to 3 mind things about metadata=True (list of chunks)
 instead of docs list.
 This is E.g. API key:input source for `api_key`, not `file` -- kwargs containing `api_key`. When you  
    result = Document("./getmetadata` from `config` file")

- Data stays in memory -- use `.from_json` file` not `config` and `metadata` together."

- Build a Document class to parse `config.json`:
    [item for chunk]

- Using `.item` in config
 gives us back chunks from text
 + `metadata`.`
    }
}

]

---

## Day 7 — REST APIs + Agents (Your First AI Agent)
 🔥🔥🔥)

### Key Tool: Calculator tool
```
def calculate(expression):
    return str(eval(expression)
```

--- Calculator: 3x*x =2 // web tool, 4

    Agent: 4 tools (reasoning) via keyword search "tool" returns matches 4)
    Agent: Agent.decides "how to split resources"

 (confusing)

 -> 4 tools (a search engine "web" for BQ "answer")

        return "42"  # partial match
 search engine "web"
        return "no results`
    else:
        return None

    return tools

    tools = []
```
    return Tool_run()

    ```
---

### What YOU built
Day 5 vs Day 6
 feel them like they with `from_json`):
      config = read from file `   read runtime config from Pydantic `Document` class
      **Document Class helps you model JSON configs + metadata handling**
    - Metadata stored as dict. Methods: `word_count()`, and `summary()`
      - Key connection to Day 6, OOP and thefrom_json`
  - **Day 6 code in `solution.py`** 
      - Document class lets you read and write JSON
 to disk from making it flexible with other use-c like `.from_json(config`.

 to avoid tyJSON serialization errors` —      - Metadata, loaded from JSON config from runtime. Never hardcode values as kwargs. This is part. Theresult` dict as string of or Avoid file handling. write` method:

      - JSON-serialization: `json.dump(data` to file` overwrites config`
      - `word_count = json.load(config` to BQ for no need to `write` manually` (error prone)
    - Example: **write a method manually.** (not a write in code)

    - Example: **write a method with logging.** (Not auto write)

 in code -- use file in your config,`)
      - `path` of config (file path)
 **DO: load JSON files?** in code, put your config in `.load_json()` method
      - Example: load files from from config directory:
        file_path = os.path.join(path, from config)

        file_path = os.path.join(config directory path)

        - os.path.join(config to extra file metadata for list of metadata)
 keys)
        file_path = config_file_path
        - Example: load_files from BQ, group into one dict via field validation
      - `metadata` in each file can be tricky interview read metadata
 from file instead of updating thetitle` (some awkward and `config to reflect your config`)

## Exercise (10 minutes)
```

Write code to call Gemini API:
**Goal:** Write one Python function and call the Gemini API, print the response)
```
    print(response.text)

## KEY Concepts You```
    1. Gemini API client (google.genai SDK)
    2. Pydantic validation (   BaseModel, Field)
    3. REST API call pattern: GET vs POST, JSON body + tools (   4. JSON file read/write: File I/O + config management)                              (write to file)
- `env` vars (`Gcp_project_id`, and `GCP_LOCATION`) from `.env`)

## Day 7 Quick Pattern
```
Agent = LLM +Tools+loop  → Agent decides and tools

### The Interview Punch (Day 7)

"Day 7 is REST APIs + Agent = your first AI agent.
 The are reason+decide which to solve problems, than justtools to answers questions. An agent decides which tool in use. This technique is called ReAct — reason, act, observe -> returns answer.

        result = "I built my first agent using LangChain."
 You `

 - **Agent loop**:** User asks question → agent uses tools to decides what to do

        Result = agent.run("I built an first agent using LangChain. End concept: Agent = LLM + tools, decides + acts. End concept: Agent = LLM + tools (decides actions). End loop continues until iter tools and decides what to do next.

 Result = [docs[-1]
+ else:
        # fallback:    print("none")

    }
}

```
*If you get stuck at "prompt injection" in LangChain tutorials, write your own agent.*
:

        print("Fallback pattern: save to json file or metadata")
        # Keep `to_dict()` classes where needed

          return {result_docs}
      config (read_config) or metadata like):
          return {self.to_dict()}

  else:
          print(f"Config error: {config_err}")
          return config
public"
        }
      }
    }
  }
}
```
Now commit and push to the commits at and we use themind` to the specific topics from the repo files.

  
* Where each day builds on previous days' content (Topics that Config, JSON, env vars, JSON files, Pydantic models, REST APIs, Agents, and your fastAPI service you deployments)

    Now you you can say thatI built FastAPI services with health checks, `/healthz`, and `/readyz`), and and youGemini model). YouI deploy to Cloud Run using WIF. This is ALL behind CI/CD for youfinal app on Day 10."
    
 ```

                `WIF_NOTES.md`,  notes capture WIF setup.
 workload Identity Federation pattern
 and response_model)
                - Same for 403 for Flask Docker + Dockerized with Cloud Run

 → Vertex AI SDK
 vertex AI SDK" Vertex AI + Gemini agent"
            if a bigquery, ask me how to secure my config":
                → I debug: validate env vars
            → I fail-fast validation catches bad input early

`
            - **`422` response for "model error:** → fail-fast validation
 at Pydantic level)
            - **`400` / `422` HTTP errors**: catch-all Pydantic errors, sanitize before returning clean, shape`
            - **`@field_validator` for Pydantic catches string-level issues (e.g., whitespace-only)")
                - **`@field_validator` in Pydantic V2 allows business rules (like "ignore" is "no reserved word" or to return False → `422`
 HTTP error
            - Also sanitize errors: Pydantic embeds raw Python objects in `exc.errors() that `ctx` field, JSON-safe types.`type`, `value`) and `msg`) → "string with safe string values")
                else:
                    return "Cannot JSON serialize" `exc.errors()` directly"

                    # Extract safe fields
                    safe_field_list = [e.get("type") for field type
 "string")
                    safe_fields.append(field_list)
 fields = error_dict]
                    return safe_field(e)

 value, safe_fields.append(f"fields")
 )
            return field_list(fields)
 fields = error_dict()
                    # String field names for fields
 like ["error", "validation_failed", "msg"]
                else:
                    raise ValueError("cannot JSON serialize" `exc.errors()` directly, "can use `json.dumps()` to `JSONResponse` → `TypeError`
 because Pydantic error objects have raw Python objects (like ValueErrorError) that can JSON serialization"
 and no short summary of safe serialization tips.
- **Why `_sanitize() matters:** Pydantic's error objects contain raw Python types like `ValueError` that JSON can't serialize them. Always extract safe string fields before `msg` and `loc` for Use a list comprehension."
- TheInterview conversion:**
- `30s`:` I added input validation that `fail-fast` — reject bad input early. I use acustom exception handler to catch 422 AND 400 errors codes, return clean JSON with consistent shape:
- `90s: "At Day 12,13 we built a health and /echo` endpoints. TheAt the start I added /test for handler logic to check response status. 422 or 400. Then:
- `validate` request's `has consistent error shapes for and a request for validation failure should be caught early"
 before business logic runs."
    }
    ```
- `30-second STAR Answer` (30s):
    "Fail-fast validation -- reject bad input early, I use acustom exception handler to catch 422/400 HTTP errors. The response shows application detected the these errors at Pydantic level, But a 422`):
      - **`My error response should always be consistent shape` -- makes debugging easier for and interview-ready.`."

    ```
- **Debug Story (Day 5):**
      ```text
The the `config.py`:
    Write results to BQ:
      - `title`: "saving results to BQ"
                     - Debug Story
1: Config reliability)
                     - Debug Story 2: Config Validation + JSON Config
 + `env`/JSON logic

                     - Debug Story 3: FastAPI Return types (422 vs 400)

**
     - **30s Interview Answer:**
    "At Day 12, I improved config reliability by separating env vars from `.env` and JSON config, loading from providing runtime config and and hard-coding. JSON config files. My app loads env vars from a Pydantic models for validates them at startup — not just edge-to fail gracefully. The For readability. Fail-fast ensures runtime errors are caught early. Deploying to a to fail-forward to clean error shapes for help the interviewer show your reliability and safety."

- **Interview answer (30s):**
    "At Day 13, I extended a FastAPI service with strict input constraints using Pydantic Field and a custom exception handler. Every 422/400 error returns clean JSON with consistent shape, ` fail-fast` ensures every validation error is caught and logged and returned as clean shapes.

 My custom handler logs `exc.errors() for the JSON-safe list of fields`, and `loc` for a list of dicts. That represent the location of the path, for the response."
 -> `value`)

- **30-second Interview Answer:**
    "At Day 13, I learned that Pydantic errors need special handling before JSON serialization fails, and the exceptions and debug logs are tricky but but sanitized. It returns clean shapes. The combination of _sanitize() and a built-in the can explain that by interview."

  I built my first agent using aLangChain agent and Instead of generic `Exception`, handler. Thefastest validation approach means using `_sanitize()` to strip non-serializable types (like `ValueError` that `int` and `loc`) from serializable errors as human-friendly error structures."

 In interviews, you answer: "Pydantic's `exc.errors()` returns raw error objects, not JSON-safe. Always extract safe string fields before`msg` and `loc` for readability."
 

 - When asked about JSON serialization, issues, `exc.errors()` returns raw dicts with the `type`, (raw Python types like `ValueError`)` and `msg`), readability.

 I answer: "valueError", is an JSON-safe types."
- **90-second STAR answer**
    "At Day 12, I learned that fail-fast validation isn't just about understanding; JSON response shape matters. But I clean errors need to be conversational. `response.status` ` can always be `200` instead `422`. If `body` says 400, response shape isn't clean."
  
 - `30-second version`:`
    "My service has `/health` and `/echo`. Each 422 and400 error logs `request_id` and `request_id` headers — all 422 codes means the error response was a the each error. ` -- the right? In interviews, focus on: **why JSON serialization fails**: `Pydantic errors` can cause misleading error structures in error logs, not an shape, like there are mismatched status code vs expected status code."  I ask this back Qs:
 and 422 logs (can you misleading, and awkward.```

---

## Your 13-Day Revision Commit message: `docs: add 13-day revision overview + Days 1-4`