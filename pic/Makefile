test:
	./sortpics.py add $(HOME)/Pictures
	sqlite3 sortpics.db  .dump

testhugo:
	rm -rf test
	hugo new site test
	cd test; git init; \
	git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke; \
	echo 'theme = "ananke"' >> config.toml
	cp -r hugo-easy-gallery/layouts test/
	cp -r hugo-easy-gallery/static test/
	mkdir -p test/static/img
	./sortpics.py copy --dest=$(CURDIR)/test/static/img
	cd test; 
	cd test; \
	for d in `cd static; find img -type d`; do \
		f="posts/$$(echo $$d | tr '/' '-').md"; \
		hugo new $$f; \
		echo "{{< load-photoswipe >}}" >> content/$$f; \
		echo "$${d}:{{< gallery dir=\"/$${d}/\" />}}" >> content/$$f; \
	done
	cd test; hugo server -D

server:
	cd test; hugo
	cd $(CURDIR)/test/public; python $(CURDIR)/server.py


prepare:
	sudo apt-get install exiftool hugo

clean:
	rm sortpics.db

.PHONY: test
