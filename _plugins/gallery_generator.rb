# frozen_string_literal: true

require 'pathname'

module Jekyll
  class GalleryPage < Page
    def initialize(site, base, folder)
      @site = site
      @base = base
      @dir = File.join('gallery', folder)
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'gallery.html')

      self.data['layout'] = 'gallery'
      self.data['gallery_folder'] = folder
      self.data['title'] = folder.split('-').map { |part| part.capitalize }.join(' ')
      self.data['permalink'] = "/gallery/#{folder}/"
      self.data['sitemap'] = false
      self.data['images'] = find_images_for(folder)
    end

    private

    def find_images_for(folder)
      root = File.join(@base, 'assets', 'images', folder)
      return [] unless Dir.exist?(root)

      Dir.glob(File.join(root, '**', '*')).select do |path|
        File.file?(path) && image_extension?(path)
      end.sort.map do |path|
        relative_path = Pathname.new(path).relative_path_from(Pathname.new(@base)).to_s
        "/#{relative_path.tr('\\', '/')}"
      end
    end

    def image_extension?(path)
      %w[.jpg .jpeg .png .webp .gif .avif .svg].include?(File.extname(path).downcase)
    end
  end

  class GalleryGenerator < Generator
    safe true
    priority :low

    def generate(site)
      root = File.join(site.source, 'assets', 'images')
      return unless Dir.exist?(root)

      folders = Array(site.config['gallery_folders']).map(&:to_s)
      folders = Dir.children(root).sort if folders.empty?

      folders.each do |folder_name|
        full_path = File.join(root, folder_name)
        next unless File.directory?(full_path)
        next if folder_name.start_with?('.')

        has_images = Dir.glob(File.join(full_path, '**', '*')).any? do |path|
          File.file?(path) && %w[.jpg .jpeg .png .webp .gif .avif .svg].include?(File.extname(path).downcase)
        end

        next unless has_images

        site.pages << GalleryPage.new(site, site.source, folder_name)
      end
    end
  end
end
