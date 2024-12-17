# scrape_w_llm
ウェブサイトを取得して解析するやつ。

実行時に下記のワーニングが出る可能性がある。<br>
<a href="https://blog.jp.square-enix.com/iteng-blog/posts/00095-vertexai-fcalling/">このサイト</a>によると大きな問題はなさそうなのでひとまず放置。<br>
```
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
E0000 00:00:1733883710.909377  865308 init.cc:229] grpc_wait_for_shutdown_with_timeout() timed out.
```
