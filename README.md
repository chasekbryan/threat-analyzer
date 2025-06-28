Threat Analyzer

A command-line tool that analyzes replies to the latest tweet of a given X (formerly Twitter) user and sorts them by a color-coded threat level.

⸻

⸻

Features
- Fetches the latest original tweet (excluding retweets and replies) of a specified X user using the Twitter API v2.
- Retrieves recent replies to that tweet via Twitter’s “search recent” endpoint.
- Classifies each reply into one of five threat levels based on configurable keyword lists:
- Blue (severity 1)
- Green (2)
- Yellow (3)
- Orange (4)
- Red (5)
- Prints a color-coded summary to the terminal.
- Optionally dumps full JSON output to a file.
- Includes a built-in smoke test mode (--test).

⸻

Prerequisites
1. Python 3.6+ (tested on 3.11)
2. A developer account on Twitter Developer Platform with a Bearer Token for API v2.
3. The Python requests library:

``` pip install requests ```



⸻

Installation
1. Clone or download this repository.
2. (Optional) Make the script executable:

``` chmod +x threat_analyzer.py ```

3. Install dependencies:

``` pip install requests ```

⸻

Configuration

The tool requires your Twitter API Bearer Token as an environment variable:

export TWITTER_BEARER_TOKEN="YOUR_BEARER_TOKEN_HERE"

To persist it across sessions, add that line to your shell startup file (~/.zshrc, ~/.bash_profile, etc.)

⸻

Usage

Basic Command

``` python3 threat_analyzer.py --user <USERNAME> --limit <N> --output <FILE.json> ```

	--user (-u): X handle to analyze (default: NSAGov).
	--limit (-n): Maximum number of replies to fetch (default: 100, max per API call: 100).
	--output (-o): Path to write full JSON results.

Options

Flag	Description
-u, --user	X username (default: NSAGov)
-n, --limit	Max number of replies (default: 100)
-k, --keywords-file	Path to JSON file mapping severity levels to keyword arrays
-o, --output	Write full results to specified JSON file
--test	Run built-in classification sanity checks and exit

⸻

Examples
1. Smoke Test (verifies classification logic):

``` python3 threat_analyzer.py --test ```
 → All tests passed.

2. Analyze 50 replies for NSA (@NSAGov):

``` python3 threat_analyzer.py \
  --user NSAGov \
  --limit 50 \
  --output threats.json
```
Output:

[Red] @someuser: “We will destroy you…”… (https://x.com/someuser/status/1234567890)
[Yellow] @another: “Be warned…”… (https://x.com/another/status/0987654321)
…

3. **Custom Keywords**:
   ```json
   {
     "5": ["obliterate","annihilate"],
     "4": ["danger"],
     "3": ["caution"],
     "2": ["alert"],
     "1": []
   }

python3 threat_analyzer.py \
  -u NSAGov \
  -n 25 \
  -k custom_keywords.json

⸻

Customization

Keyword File

To override the default keyword mapping, create a JSON file where keys are severity levels ("1"–"5") and values are arrays of substring keywords. Example (keywords.json):

{
  "5": ["kill","destroy","bomb"],
  "4": ["threat","harm"],
  "3": ["warn","danger"],
  "2": ["caution","alert"],
  "1": []
}

Then run:

``` python3 threat_analyzer.py -u NSAGov -n 50 -k keywords.json ```

The tool will fallback to defaults if the file fails to load.

⸻

Running Tests

Use the --test flag to exercise built-in smoke tests:

``` python3 threat_analyzer.py --test ```
 → All tests passed.

⸻

Troubleshooting
- Error: Set environment variable TWITTER_BEARER_TOKEN
You must export your Twitter API v2 bearer token before running.
- HTTP errors (401, 403, etc.)
Ensure your token is valid and has the necessary “read Tweets” permissions.
- max_results limit
The Twitter API v2 restricts max_results to 100 per call.
- Network/SSL Errors
Make sure your system’s CA bundle is up-to-date or use a managed Python distribution.

⸻

License

This project is released under the GPL3 License. 
