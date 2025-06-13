# Command-line API Reference

The processor is controlled entirely from the command line.  All functionality
is available via the module-path entrypoint so you can run either of the
following forms:

```bash
python -m scripts.data_processing.sentiment_processor [OPTIONS]
./scripts/data_processing/sentiment_processor.py   [OPTIONS]
```

---

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--config, -c` | path | – | JSON config file (alternative to CLI flags) |
| `--query, -q`  | string | **required** | Search query / subreddit list (comma-separated) |
| `--sources`    | list  | `reddit,twitter` | Data sources to use (subset of `reddit`, `twitter`) |
| `--models`     | list  | `vader` | Sentiment models to use (`vader`, `gpt4`, `claude`, `gemini`, `gemma`) |
| `--days-back`  | int   | `7` | Number of days of history to fetch |
| `--max-posts`  | int   | `100` | Maximum posts per source |
| `--output-format` | choice | `json` | `json`, `csv`, or `sqlite` |
| `--output-path`  | path | `./results` | Directory (or file for sqlite) in which to place outputs |
| `--include-images` | flag | off | Enable image sentiment analysis (adds vision model calls) |
| `--dry-run` | flag | off | Print config & exit – no processing |

### JSON Config structure

The dataclass equivalent is `ProcessingConfig` in `sentiment_processor.py`.
If `--config path.json` is supplied the CLI flags (other than `--dry-run`) are
ignored.

```json
{
  "query": "python,programming",
  "sources": ["reddit", "twitter"],
  "models": ["vader", "gpt4"],
  "start_date": "2025-01-01T00:00:00Z",
  "end_date":   "2025-01-07T00:00:00Z",
  "include_images": false,
  "max_posts": 200,
  "output_format": "json",
  "output_path": "./results"
}
```

---

## Environment variables

| Variable | Required for | Description |
|----------|--------------|-------------|
| `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` / `REDDIT_USER_AGENT` | Reddit | Personal-use script credentials from <https://www.reddit.com/prefs/apps> |
| `TWITTER_BEARER_TOKEN` | Twitter | Twitter API v2 bearer token |
| `OPENAI_API_KEY` | GPT-4 / GPT-4 Vision | Secret key from <https://platform.openai.com> |
| `ANTHROPIC_API_KEY` | Claude 3 | Claude and Claude Vision |
| `GOOGLE_API_KEY` | Gemini | Gemini Pro & Gemini Pro Vision |

If any key is missing the corresponding model/source gracefully degrades to a
fallback or returns `0` scores – the script **never crashes** due to missing
secrets.

---

## Output formats

### JSON
Hierarchical structure:
```json
{
  "analysis_summary": { ... },
  "results": [ { <SentimentResult-like dict> }, ... ]
}
```

### CSV
Matches the web-app export:
`ID,Content,Score,Post Date,Perceived IQ,Bot Probability,Source Type,Post ID,Manual Sentiment,Override Reason`

### SQLite
A file containing a single table `sentiment_results` with columns mirroring the
CSV header plus both `score` and `compound_score`.