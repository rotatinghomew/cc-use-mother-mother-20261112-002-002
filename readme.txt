测试：python3 -m unittest discover -s tests/fusion_surfaces -p 'test_*.py'
构建：python3 -m compileall -q village_rain_fusion tests/fusion_surfaces
验收：python3 -m village_rain_fusion.products.command fixtures/demo.json --database /tmp/village_rain_fusion-acceptance.sqlite3
