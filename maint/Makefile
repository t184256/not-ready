DESTDIR ?= ./
HOME ?= FONTCONFIG_HOME

PREPROCESSOR = maint/preprocess.py
VERSCRIPT := maint/version.py
CHECK_LANGUAGETOOL := maint/languagetool.py
CHECK_LIZARD_WC := maint/lwc.py
CHECK_WC := maint/wc.py
CHECK_RATCHET := maint/ratchet.py

META_EN = maint/metadata.en.yml
STYLING_EN_EPUB = maint/styling.en.epub.yml
STYLING_EN_FB2 = maint/styling.en.fb2.yml
STYLING_EN_PDF = maint/styling.en.pdf.yml
LDICT_EN = maint/ldict.en.yml
LTEX_EN += .ltex/ltex.dictionary.ru-RU.txt
LTEX_EN += .ltex/ltex.disabledRules.ru-RU.txt
LTEX_EN += .ltex/ltex.hiddenFalsePositives.ru-RU.txt

META_RU = maint/metadata.ru.yml
STYLING_RU_EPUB = maint/styling.ru.epub.yml
STYLING_RU_FB2 = maint/styling.ru.fb2.yml
STYLING_RU_PDF = maint/styling.ru.pdf.yml
LDICT_RU = maint/ldict.ru.yml
LTEX_RU += .ltex/ltex.dictionary.ru-RU.txt
LTEX_RU += .ltex/ltex.disabledRules.ru-RU.txt
LTEX_RU += .ltex/ltex.hiddenFalsePositives.ru-RU.txt

CHAPTERS_EN += text/en/01-qualified.md
CHAPTERS_EN += text/en/02-allied.md
CHAPTERS_EN += text/en/03-understood.md
CHAPTERS_EN += text/en/04-organized.md
CHAPTERS_EN += text/en/05-resolved.md
CHAPTERS_EN += text/en/06-controlled.md
CHAPTERS_EN += text/en/07-entrusted.md
CHAPTERS_EN += text/en/08-principled.md
CHAPTERS_EN += text/en/09-settled.md
CHAPTERS_EN += text/en/10-cultured.md
CHAPTERS_EN += text/en/11-disciplined.md
CHAPTERS_EN += text/en/12-commended.md
#CHAPTERS_EN += text/en/99-real.md

CHAPTERS_RU += text/ru/01-qualified.md
CHAPTERS_RU += text/ru/02-allied.md
CHAPTERS_RU += text/ru/03-understood.md
CHAPTERS_RU += text/ru/04-organized.md
CHAPTERS_RU += text/ru/05-resolved.md
CHAPTERS_RU += text/ru/06-controlled.md
CHAPTERS_RU += text/ru/07-entrusted.md
CHAPTERS_RU += text/ru/08-principled.md
CHAPTERS_RU += text/ru/09-settled.md
CHAPTERS_RU += text/ru/10-cultured.md
CHAPTERS_RU += text/ru/11-disciplined.md
CHAPTERS_RU += text/ru/12-commended.md
#CHAPTERS_RU += text/ru/99-real.md

VERFILE := $(DESTDIR)/.version

.PHONY: outputs
outputs: $(DESTDIR)/not-ready.en.80column.txt
outputs: $(DESTDIR)/not-ready.ru.80column.txt
outputs: $(DESTDIR)/not-ready.en.freeflow.txt
outputs: $(DESTDIR)/not-ready.ru.freeflow.txt
outputs: $(DESTDIR)/not-ready.en.pdf
outputs: $(DESTDIR)/not-ready.ru.pdf
outputs: $(DESTDIR)/not-ready.en.epub
outputs: $(DESTDIR)/not-ready.ru.epub
outputs: $(DESTDIR)/not-ready.en.fb2
outputs: $(DESTDIR)/not-ready.ru.fb2
outputs: $(DESTDIR)/not-ready.en-ru.interleaved.pdf
all: outputs
clean:
	rm -f $(DESTDIR)/not-ready.en.80column.txt
	rm -f $(DESTDIR)/not-ready.ru.80column.txt
	rm -f $(DESTDIR)/not-ready.en.freeflow.txt
	rm -f $(DESTDIR)/not-ready.ru.freeflow.txt
	rm -f $(DESTDIR)/not-ready.en.epub.md $(DESTDIR)/not-ready.en.epub
	rm -f $(DESTDIR)/not-ready.ru.epub.md $(DESTDIR)/not-ready.ru.epub
	rm -f $(DESTDIR)/not-ready.en.fb2.md $(DESTDIR)/not-ready.en.fb2
	rm -f $(DESTDIR)/not-ready.ru.fb2.md $(DESTDIR)/not-ready.ru.fb2
	rm -f $(DESTDIR)/not-ready.en.pdf.md $(DESTDIR)/not-ready.en.pdf
	rm -f $(DESTDIR)/not-ready.ru.pdf.md $(DESTDIR)/not-ready.ru.pdf
	rm -f $(DESTDIR)/not-ready.en.intrl.pdf not-ready.ru.intrl.pdf
	rm -f $(DESTDIR)/not-ready.en-ru.interleaved.pdf
	rm -f $(DESTDIR)/.version
	rm -f $(DESTDIR)/.check-lt-en $(DESTDIR)/.check-lt-ru
	rm -f $(DESTDIR)/.check-lwc-ru $(DESTDIR)/.check-lwc-en
	rm -f $(DESTDIR)/.check-wc $(DESTDIR)/.check-ratchet

$(DESTDIR):
	mkdir -p $(DESTDIR)

$(VERFILE): $(VERSCRIPT) $(DESTDIR) $(PREPROCESSOR) $(LDICT_EN) $(LDICT_RU)
$(VERFILE): $(META_EN) $(CHAPTERS_EN) $(STYLING_EN_FB2) $(STYLING_EN_PDF)
$(VERFILE): $(META_RU) $(CHAPTERS_RU) $(STYLING_RU_FB2) $(STYLING_RU_PDF)
	$(VERSCRIPT) -u $@

$(DESTDIR)/not-ready.en.80column.txt: $(PREPROCESSOR) $(LDICT_EN) $(VERFILE)
$(DESTDIR)/not-ready.en.80column.txt: $(META_EN) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format 80column.txt \
		--dict $(LDICT_EN) \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		$(CHAPTERS_EN) > $@

$(DESTDIR)/not-ready.ru.80column.txt: $(PREPROCESSOR) $(LDICT_RU) $(VERFILE)
$(DESTDIR)/not-ready.ru.80column.txt: $(META_RU) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format 80column.txt \
		--dict $(LDICT_RU) \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		$(CHAPTERS_RU) > $@

$(DESTDIR)/not-ready.en.freeflow.txt: $(PREPROCESSOR) $(LDICT_EN) $(VERFILE)
$(DESTDIR)/not-ready.en.freeflow.txt: $(META_EN) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format freeflow.txt \
		--dict $(LDICT_EN) \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		$(CHAPTERS_EN) > $@

$(DESTDIR)/not-ready.ru.freeflow.txt: $(PREPROCESSOR) $(LDICT_RU) $(VERFILE)
$(DESTDIR)/not-ready.ru.freeflow.txt: $(META_RU) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format freeflow.txt \
		--dict $(LDICT_RU) \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		$(CHAPTERS_RU) > $@

$(DESTDIR)/not-ready.en.epub.md: $(PREPROCESSOR) $(LDICT_EN)
$(DESTDIR)/not-ready.en.epub.md: $(VERFILE)
$(DESTDIR)/not-ready.en.epub.md: $(META_EN) $(STYLING_EN_FB2) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format epub \
		--dict $(LDICT_EN) \
		--book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		--no-process $(STYLING_EN_FB2) \
		$(CHAPTERS_EN) > $@

$(DESTDIR)/not-ready.ru.epub.md: $(PREPROCESSOR) $(LDICT_RU)
$(DESTDIR)/not-ready.ru.epub.md: $(VERFILE)
$(DESTDIR)/not-ready.ru.epub.md: $(META_RU) $(STYLING_RU_FB2) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format epub \
		--dict $(LDICT_RU) \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		--no-process $(STYLING_RU_FB2) \
		$(CHAPTERS_RU) > $@

$(DESTDIR)/not-ready.en.epub: $(DESTDIR)/not-ready.en.epub.md
	pandoc $(DESTDIR)/not-ready.en.epub.md -o $@

$(DESTDIR)/not-ready.ru.epub: $(DESTDIR)/not-ready.ru.epub.md
	pandoc $(DESTDIR)/not-ready.ru.epub.md -o $@

$(DESTDIR)/not-ready.en.fb2.md: $(PREPROCESSOR) $(LDICT_EN)
$(DESTDIR)/not-ready.en.fb2.md: $(VERFILE)
$(DESTDIR)/not-ready.en.fb2.md: $(META_EN) $(STYLING_EN_FB2) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format fb2 \
		--dict $(LDICT_EN) \
		--book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		--no-process $(STYLING_EN_FB2) \
		$(CHAPTERS_EN) > $@

$(DESTDIR)/not-ready.ru.fb2.md: $(PREPROCESSOR) $(LDICT_RU)
$(DESTDIR)/not-ready.ru.fb2.md: $(VERFILE)
$(DESTDIR)/not-ready.ru.fb2.md: $(META_RU) $(STYLING_RU_FB2) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format fb2 \
		--dict $(LDICT_RU) \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		--no-process $(STYLING_RU_FB2) \
		$(CHAPTERS_RU) > $@

$(DESTDIR)/not-ready.en.fb2: $(DESTDIR)/not-ready.en.fb2.md
	pandoc $(DESTDIR)/not-ready.en.fb2.md -o $@

$(DESTDIR)/not-ready.ru.fb2: $(DESTDIR)/not-ready.ru.fb2.md
	pandoc $(DESTDIR)/not-ready.ru.fb2.md -o $@

$(DESTDIR)/not-ready.en.pdf.md: $(PREPROCESSOR) $(LDICT_EN)
$(DESTDIR)/not-ready.en.pdf.md: $(META_EN) $(STYLING_EN_PDF) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format pdf \
		--dict $(LDICT_EN) \
		--no-process $(META_EN) \
		--no-process $(STYLING_EN_PDF) \
		$(CHAPTERS_EN) > $@

$(DESTDIR)/not-ready.ru.pdf.md: $(PREPROCESSOR) $(LDICT_RU)
$(DESTDIR)/not-ready.ru.pdf.md: $(META_RU) $(STYLING_RU_PDF) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format pdf \
		--dict $(LDICT_RU) \
		--no-process $(META_RU) \
		--no-process $(STYLING_RU_PDF) \
		$(CHAPTERS_RU) > $@

$(DESTDIR)/not-ready.en.pdf: $(DESTDIR)/not-ready.en.pdf.md $(VERFILE)
	pandoc --pdf-engine=xelatex \
	       --metadata=subtitle:v$(shell cat $(VERFILE)) \
	       $(DESTDIR)/not-ready.en.pdf.md -o $@

$(DESTDIR)/not-ready.ru.pdf: $(DESTDIR)/not-ready.ru.pdf.md $(VERFILE)
	pandoc --pdf-engine=xelatex \
	       --metadata=subtitle:v$(shell cat $(VERFILE)) \
	       $(DESTDIR)/not-ready.ru.pdf.md -o $@

# a 'debugging' version
$(DESTDIR)/not-ready.en.intrl.pdf: maint/pad.en $(DESTDIR)/not-ready.en.pdf
	cpdf -pad-after $(DESTDIR)/not-ready.en.pdf $$(cat maint/pad.en) -o $@

$(DESTDIR)/not-ready.ru.intrl.pdf: maint/pad.ru $(DESTDIR)/not-ready.ru.pdf
	cpdf -pad-after $(DESTDIR)/not-ready.ru.pdf $$(cat maint/pad.ru) -o $@

$(DESTDIR)/not-ready.en-ru.interleaved.pdf: $(DESTDIR)/not-ready.en.intrl.pdf
$(DESTDIR)/not-ready.en-ru.interleaved.pdf: $(DESTDIR)/not-ready.ru.intrl.pdf
	cpdf \
	     -collate \
	     $(DESTDIR)/not-ready.en.intrl.pdf \
	     $(DESTDIR)/not-ready.ru.intrl.pdf \
	     AND \
	     -twoup-stack \
	     AND \
	     -rotate 90 \
	     -o $@


### checks

check: $(DESTDIR)/.check-lt-ru $(DESTDIR)/.check-lt-en
check: $(DESTDIR)/.check-lwc-ru $(DESTDIR)/.check-lwc-en
check: $(DESTDIR)/.check-wc $(DESTDIR)/.check-ratchet
.PHONY: check
all: check


CHECK_WC := maint/wc.py
CHECK_RATCHET := maint/ratchet.py

$(DESTDIR)/.check-lt-en: $(CHECK_LANGUAGETOOL) $(LTEX_EN) $(CHAPTERS_EN)
	$(CHECK_LANGUAGETOOL) --lang en-GB --unused=error $(CHAPTERS_EN)
	touch $@

$(DESTDIR)/.check-lt-ru: $(CHECK_LANGUAGETOOL) $(LTEX_RU) $(CHAPTERS_RU)
	$(CHECK_LANGUAGETOOL) --lang ru-RU --unused=error $(CHAPTERS_RU)
	touch $@

$(DESTDIR)/.check-lwc-en: $(CHECK_LIZARD_WC) $(LDICT_EN) $(CHAPTERS_EN)
	$(CHECK_LIZARD_WC) --lang en --dict $(LDICT_EN) $(CHAPTERS_EN)
	touch $@

$(DESTDIR)/.check-lwc-ru: $(CHECK_LIZARD_WC) $(LDICT_RU) $(CHAPTERS_RU)
	$(CHECK_LIZARD_WC) --lang ru --dict $(LDICT_RU) $(CHAPTERS_RU)
	touch $@

$(DESTDIR)/.check-wc: $(CHECK_WC) $(CHAPTERS_EN) $(CHAPTERS_RU)
	$(CHECK_WC)
	touch $@

$(DESTDIR)/.check-ratchet: $(CHECK_RATCHET) $(CHAPTERS_EN) $(CHAPTERS_RU)
$(DESTDIR)/.check-ratchet: $(LDICT_EN) $(LDICT_RU)
	$(CHECK_RATCHET)
	touch $@
