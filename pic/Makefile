test:
	./sortpics.py add t
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
	cp -r t test/static/img/t
	cd test; hugo new posts/my-first-post.md;
	cd test; \
	echo "{{< load-photoswipe >}}" >> content/posts/my-first-post.md; \
	for d in `cd static; find img -type d`; do \
		echo "$${d}:{{< gallery dir=\"/$${d}/\" />}}" >> content/posts/my-first-post.md; \
	done
	cd test; hugo server -D

prepare:
	sudo apt-get install exiftools hugo

clean:
	rm sortpics.db
