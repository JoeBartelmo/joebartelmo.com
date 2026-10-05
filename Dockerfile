FROM ruby:3.3.6-bullseye

WORKDIR /srv/jekyll

ENV BUNDLE_PATH=/usr/local/bundle \
    BUNDLE_APP_CONFIG=/usr/local/bundle/config \
    JEKYLL_ENV=development

COPY Gemfile* ./
RUN bundle install

COPY assets/ ./assets/
COPY _data/ ./_data/
COPY _includes/ ./_includes/
COPY _pages/ ./_pages/
COPY _posts/ ./_posts/
COPY index.html ./
COPY favicon.ico ./
COPY _config.yml ./
COPY CNAME ./
COPY resume.html ./

EXPOSE 4000

CMD ["bash", "-lc", "bundle exec jekyll serve --host 0.0.0.0 --port 4000 --trace --livereload"]
