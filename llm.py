import json
import os
import urllib.request
import urllib.error
from models import PerformanceSummary


SYSTEM_MESSAGE = (
    "Analyze trading strategy performance metrics. "
    "Base your analysis only on the metrics provided — do not assume or infer "
    "information that is not explicitly given. "
    "Be concise, data-driven, and actionable."
)

USER_TEMPLATE = """\
The following performance metrics come from a momentum / trend-following equity strategy:

  Total Trades:          {total_trades}
  Win Rate:              {win_rate:.2f}%
  Expectancy (R):        {expectancy_r:.2f}
  Average R:             {average_r:.2f}
  Avg Win R:             {average_win_r:.2f}
  Avg Loss R:            {average_loss_r:.2f}
  Profit Factor:         {profit_factor:.2f}
  Largest Win R:         {largest_win_r:.2f}
  Largest Loss R:        {largest_loss_r:.2f}
  Std Dev R:             {std_dev_r:.2f}
  Max Consec. Losses:    {max_consec_losses}
  Max Drawdown:          {max_drawdown:.2f}%

Based only on the metrics above, provide a concise structured analysis covering:
1. Structural strengths
2. Structural weaknesses
3. Risk profile
4. Long-term consistency
5. Areas for improvement

Do not assume any context beyond what is provided.
Keep the response short — roughly 150 to 250 words, suitable for embedding in a Markdown report.
Use numbered sections and line breaks for readability.
"""

API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o"
TIMEOUT_SECONDS = 30


def _build_user_message(s: PerformanceSummary) -> str:
    return USER_TEMPLATE.format(
        total_trades=s.total_trades,
        win_rate=s.win_rate * 100,
        expectancy_r=s.expectancy_r,
        average_r=s.average_r,
        average_win_r=s.average_win_r,
        average_loss_r=s.average_loss_r,
        profit_factor=s.profit_factor,
        largest_win_r=s.largest_win_r,
        largest_loss_r=s.largest_loss_r,
        std_dev_r=s.std_dev_r,
        max_consec_losses=s.max_consecutive_losses,
        max_drawdown=s.max_drawdown_percent * 100,
    )


def _chat_completion(api_key: str, system_msg: str, user_msg: str) -> str:
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
    payload = json.dumps({
        "model": model,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
    }).encode()

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read())
        return body["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"OpenAI API returned HTTP {e.code}: {e.read().decode()}") from e


def generate_narrative(summary: PerformanceSummary) -> str | None:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("[info] OPENAI_API_KEY not set — skipping LLM diagnostics.")
        return None

    try:
        return _chat_completion(api_key, SYSTEM_MESSAGE, _build_user_message(summary))
    except Exception as e:
        print(f"[warn] LLM diagnostics failed: {e}")
        return None
