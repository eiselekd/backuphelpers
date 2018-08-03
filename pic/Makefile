test:
	./sortpics.py add $(HOME)/Pictures
	sqlite3 sortpics.db  .dump

themedir:
	if [ ! -d themes ]; then \
		git clone --recursive https://github.com/spf13/hugoThemes.git themes; \
	fi

hugo:
	#cp -r t/2013-08-16 hugo/static/data/
	#cp -r t/2013-10-10 hugo/static/data/
	# hugo/static/data needs to contain pictures directories of format
	# hugo/static/data/album1/photos
	# hugo/static/data/album2/photos
	# ...
	python3 gengallery.py --hugo hugo/content/img/ hugo/static/data/
	cd hugo; hugo

server:
	cd $(CURDIR)/test/public; python $(CURDIR)/server.py

gen:
	python gengallery.py t/

#
# cd $(CURDIR)/test/; hugo

prepare:
	sudo apt-get install exiftool hugo

clean:
	rm sortpics.db

.PHONY: test hugo
