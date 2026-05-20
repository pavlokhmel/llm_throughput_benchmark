import argparse
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
import sys

def make_request(api_url, api_key, model, prompt, headers):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    data = json.dumps(payload).encode("utf-8")
    
    request_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    if headers:
        for h in headers:
            if "=" in h:
                k, v = h.split("=", 1)
                request_headers[k] = v

    req = urllib.request.Request(api_url, data=data, headers=request_headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=3000) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="LLM Throughput Benchmark")
    parser.add_argument("--api-url", required=True, help="Full URL of the chat completions endpoint")
    parser.add_argument("--api-key", default="", help="API Key")
    parser.add_argument("--model", required=True, help="Model name")
    parser.add_argument("--prompt", help="Prompt text")
    parser.add_argument("--requests", type=int, default=1, help="Total number of requests")
    parser.add_argument("--parallel", type=int, default=1, help="Number of concurrent requests")
    parser.add_argument("--verbose", action="store_true", help="Show full output")
    parser.add_argument("--no-header", action="store_false", dest="header", default=True, help="Hide column names in one line output")
    parser.add_argument("--parsable", action="store_true", help="Output in tab-separated format for parsing")
    
    args = parser.parse_args()

    prompt = args.prompt
    if not prompt:
        print("Error: --prompt is required", file=sys.stderr)
        sys.exit(1)

    results = []
    start_time = time.perf_counter()
    
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = [executor.submit(make_request, args.api_url, args.api_key, args.model, prompt, None) for _ in range(args.requests)]
        for future in futures:
            results.append(future.result())

    end_time = time.perf_counter()
    total_time = end_time - start_time

    success_count = 0
    total_prompt_tokens = 0
    total_completion_tokens = 0

    for res in results:
        if "error" in res:
            if args.verbose:
                print(f"Request failed: {res['error']}")
        else:
            success_count += 1
            if args.verbose:
                print(json.dumps(res, indent=2))
            
            usage = res.get("usage", {})
            total_prompt_tokens += usage.get("prompt_tokens", 0)
            total_completion_tokens += usage.get("completion_tokens", 0)

    tok_per_sec = total_completion_tokens / total_time if total_time > 0 else 0

    headers = ["MODEL", "TOK/S", "TIME(S)", "IN_TOK", "OUT_TOK", "REQUESTS", "PARALLEL", "SUCCESS"]
    values = [args.model, str(int(tok_per_sec)), str(int(total_time)), str(total_prompt_tokens), str(total_completion_tokens), str(args.requests), str(args.parallel), str(success_count)]

    if args.parsable:
        if args.header:
            print("\t".join(headers))
        print("\t".join(values))
    else:
        widths = [max(len(h), len(v)) for h, v in zip(headers, values)]
        
        if args.header:
            print("  ".join(f"{h:<{widths[i]}}" for i, h in enumerate(headers)))
        
        print("  ".join(f"{v:<{widths[i]}}" for i, v in enumerate(values)))

if __name__ == "__main__":
    main()