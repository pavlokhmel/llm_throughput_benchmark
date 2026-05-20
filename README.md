# LLM throughput benchmark

This is a simple LLM throughput benchmark. It is written in Python, and it uses only standard library without external dependencies. I  tried to keep it below 100 lines.

Prompt is short and it tries to push model to generate long output to get tok/s.

Available arguments:
```
  -h, --help           show this help message and exit
  --api-url API_URL    Full URL of the chat completions endpoint
  --api-key API_KEY    API Key
  --model MODEL        Model name
  --prompt PROMPT      Prompt text
  --requests REQUESTS  Total number of requests
  --parallel PARALLEL  Number of concurrent requests
  --verbose            Show full output
  --no-header          Hide column names in one line output
  --parsable           Output in tab-separated format for parsing
```

Example command and output with headers:

```
$ python3 llm_throughput_benchmark.py --api-url http://127.0.0.1:8080/v1/chat/completions --model ggml-org/gemma-4-E2B-it-GGUF --prompt "Provide a comprehensive, highly verbose technical guide on LLMs covering history, transformer architecture, tokenization, pre-training, reinforcement learning from human feedback, limitations, and future trends. Expand each section with extreme detail." --requests 1 --parallel 1                      
MODEL                         TOK/S  TIME(S)  IN_TOK  OUT_TOK  REQUESTS  PARALLEL  SUCCESS
ggml-org/gemma-4-E2B-it-GGUF  48     90       59      4424     1         1         1
```

Example with API key without headers and parsable output (tab separator):
```
$ export LLM_API_KEY=sk-v..........Q

$ python3 llm_throughput_benchmark.py --api-url http://127.0.0.1:8080/v1/chat/completions --api-key $LLM_API_KEY --model ggml-org/gemma-4-E2B-it-GGUF --prompt "Provide a comprehensive, highly verbose technical guide on LLMs covering history, transformer architecture, tokenization, pre-training, reinforcement learning from human feedback, limitations, and future trends. Expand each section with extreme detail." --requests 1 --parallel 1 --parsable --no-header
ggml-org/gemma-4-E2B-it-GGUF	48	100	59	4903	1	1	1
```
