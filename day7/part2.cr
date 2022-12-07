lines = File.read_lines("input.txt")
directory_structure = parse_file(lines)

all_sizes = [] of Int32

find_sub_directories_sizes start_directory: directory_structure, sizes_collection: all_sizes

disk_size = 70000000
unused_space_needed = 30000000

answer_total = 0

total_used_space = all_sizes.max
current_free_space = disk_size - total_used_space

all_sizes.sort.each do |dir_size|
  if current_free_space + dir_size >= unused_space_needed
    puts dir_size
    break
  end
end

class Directory
  property parent : (Directory | Nil) = nil
  property sub_directories = {} of String => Directory
  property total_file_sizes = 0

  def initialize(@parent)
  end
end

def find_sub_directories_sizes(start_directory : Directory, sizes_collection : Array(Int32))
  sub_dirs_total_size = 0

  start_directory.sub_directories.values.each do |sub_dir|
    sub_dirs_total_size += find_sub_directories_sizes sub_dir, sizes_collection
  end

  this_dir_total_size = start_directory.total_file_sizes + sub_dirs_total_size
  sizes_collection.push this_dir_total_size

  this_dir_total_size
end

def parse_file(lines : Array(String))
  root_directory = Directory.new parent: nil
  current_directory = root_directory

  line_index = 1 # skip line 0 as it's just cd /

  while line_index < lines.size
    current_line = lines[line_index]
    if current_line.starts_with?("$")
      if current_line == "$ ls"
        line_index = read_ls_output from_lines: lines, line_index: line_index + 1, into_directory: current_directory
      elsif current_line == "$ cd .."
        if parent = current_directory.parent
          current_directory = parent
        else
          raise "Tried to cd .. above root"
        end
      elsif current_line.starts_with?("$ cd")
        dir_to_enter = current_line[5, current_line.size]
        current_directory = current_directory.sub_directories[dir_to_enter]
      end
      line_index += 1
    end
  end

  root_directory
end

def read_ls_output(from_lines : Array(String), line_index : Int32, into_directory : Directory)
  current_line = from_lines[line_index]

  while !current_line.starts_with?("$")
    line_parts = current_line.split

    if line_parts[0] == "dir"
      into_directory.sub_directories[line_parts[1]] ||= Directory.new parent: into_directory
    else
      into_directory.total_file_sizes += line_parts[0].to_i
    end

    line_index += 1
    if line_index >= from_lines.size
      break
    end

    current_line = from_lines[line_index]
  end

  line_index - 1
end
