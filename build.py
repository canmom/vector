from num2words import num2words
import argparse
from glob import glob
import markdown
from markdown.extensions.smarty import SmartyExtension
from jinja2 import Environment, FileSystemLoader
import subprocess

parser = argparse.ArgumentParser(description = 'Build VECTOR chapters to html and epub.')
parser.add_argument('nChapters',type=int,help="Number of chapters to generate.",default=None,nargs='?')
parser.add_argument('nLinked',type=int,help="Number of chapters to link with navigation.",default=None,nargs='?')
parser.add_argument('--noEpilogues',dest='epilogues',action='store_const',const=False,default=True,help="Do not include epilogues in chapter sequence.")

args = parser.parse_args()

chapter_filename_format = "ch{}"
source_prefix = "VECTOR-"
source_suffix = '.md'
target_suffix = '.html'

if args.nChapters is None:
    # set the number of chapters to the number of correctly formatted chapters in the working directory if not specified
    args.nChapters = len(glob(source_prefix+chapter_filename_format.format('*')+source_suffix))

if args.nLinked is None or args.nLinked > args.nChapters:
    # default to linking all chapters
    args.nLinked = args.nChapters

with open('navigation.html') as f:
    navigation = f.read()

md = markdown.Markdown(extensions=[SmartyExtension(substitutions={
    'left-single-quote': '‘',
    'right-single-quote': '’',
    'left-double-quote': '“',
    'right-double-quote': '”',
    'left-angle-quote': '«',
    'right-angle-quote': '»',
    'ellipsis': '…',
    'ndash': '–',
    'mdash': '—'
})], output_format='html5')

jinja = Environment(loader=FileSystemLoader('.')).get_template('chapter_template.html')

class Chapter:
    def __init__(self, index, title=None, source_file=None):
        self.index = index
        if title is not None:
            self.title = title
        if source_file is not None:
            self.source_file = source_prefix+source_file+source_suffix
            with open(self.source_file) as s:
                self.source = s.read()
            self.target = source_file+target_suffix

    def __eq__(self, other):
        return self.index == other.index

    def __repr__(self):
        return "Chapter({},title='{}',source_file='{}')".format(self.index,self.title,self.source_file)

    def process_markdown(self):
        self.html = md.convert(self.source)
        md.reset()

chapters = [
    Chapter(
        index,
        title='chapter ' + num2words(index, ordinal=True).upper(),
        source_file=chapter_filename_format.format(index)
    )
    for index in range(1, args.nChapters+1)]

def insertChapter(chapter, after):
    chapters.insert(chapters.index(Chapter(after))+1, chapter)

epilogueOffset = 0
if args.epilogues:
    if args.nChapters >= 4:
        insertChapter(
            Chapter(
                4.1,
                title='segment ABDOMINAL::EPILOGUE',
                source_file='s1e'),
            4)

    if args.nLinked >= 4:
        epilogueOffset += 1

    if args.nChapters >= 8:
        insertChapter(
            Chapter(
                8.1,
                title='segment THORACIC::EPILOGUE',
                source_file='s2e'),
            8)

    if args.nLinked >= 4:
        epilogueOffset += 1

for index, chapter in enumerate(chapters):
    chapter.process_markdown()
    with open(chapter.target, 'w') as output:
        print('Building {}'.format(chapter.title))
        output.write(jinja.render(
            html=chapter.html,
            title=chapter.title,
            next=(chapters[index+1] if index != args.nLinked -1 + epilogueOffset else None),
            prev=(chapters[index-1] if index != 0 else None)
        ))

subprocess.check_call(['pandoc', 'epub-meta.txt', *[chapter.source_file for chapter in chapters], '-o', 'VECTORch1-{}.epub'.format(args.nChapters), '--epub-chapter-level=2', '--top-level-division=chapter'])
print('Generated ePub')
subprocess.run(['zip', 'VECTORch1-{}.zip'.format(args.nChapters), *[chapter.target for chapter in chapters], 'index.html', 'style.css', 'epub-cover.png', 'logo.svg'])
print('Zipped HTML')