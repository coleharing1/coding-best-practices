# Browser Verify

Verify the current browser-visible workflow end to end.

Steps:

1. identify the correct local URL and auth lane
2. confirm whether this should use the real user lane or the agent lane
3. load the page and inspect for console/runtime failures
4. exercise the target flow
5. report exact pass/fail results, screenshots if useful, and the next likely fix path

Do not pretend browser verification happened if the page was not actually opened and checked.
