#!/usr/bin/python3

import argparse
import json
import shutil
import sys
import zlib
import os.path
import xml.etree.ElementTree

print("EmulationStation to RetroArch playlists converter")

parser = argparse.ArgumentParser(description='Convert EmulationStation gamelist.xml to RetroArch playlists.')
parser.add_argument('infile', metavar='gamelist.xml', type=argparse.FileType('r', encoding='Latin-1'), help='name of input file in EmulationStation gamelist.xml format')
parser.add_argument('outfile', metavar='output.lpl', type=argparse.FileType('x', encoding='Latin-1'), help='name of file to be created in RetroArch playlist .lpl format')
parser.add_argument('-folder', nargs=1, help='only include games in folder FOLDER')
parser.add_argument('-subfolders', action='store_true', help='include games in subfolders')
parser.add_argument('-favonly', action='store_true', help='only include games marked as favorites')
parser.add_argument('-includehidden', action='store_true', help='include games marked as hidden')
parser.add_argument('-checkfiles', action='store_true', help='only include game files that are present (check is always done in working directory)')
parser.add_argument('-crc32', action='store_true', help='calculate CRC32 of game files')
parser.add_argument('-basepath', nargs=1, help='use BASEPATH instead of working directory for paths to games in the output file')
parser.add_argument('-dbname', nargs=1, help='include db_name field with value DBNAME in the output file')
parser.add_argument('-copypics', metavar=('FIELD', 'DIR'), nargs=2, help='copy pictures/videos from gamelist.xml field FIELD (e.g. image) to directory DIR')
parser.add_argument('-header', metavar='JSON', nargs=1, help='place JSON in header of output.lpl')
if len(sys.argv) < 2:
	parser.print_help()
	sys.exit(0)
args = parser.parse_args()

basepath = args.basepath[0] if args.basepath != None else None
if basepath != None and basepath[-1:] != '/' and basepath[-1:] != '\\':
	basepath += '/' if basepath[:1] == '/' else '\\'

gamelist = xml.etree.ElementTree.parse(args.infile).getroot()
result = {
	'version': '1.0'
}
if args.header != None:
	result.update(json.loads(args.header[0]))
result['items'] = []

print("Converting...")

for game in gamelist.findall('./game'):
	name = game.findtext('name')
	path = game.findtext('path')
	if name == None or name == '':
		name = os.path.splitext(os.path.basename(path))[0]
	pathclean = path[2:] if path.startswith('./') or path.startswith('.\\') else path
	if ((args.folder == None or pathclean.startswith(args.folder[0]+'/') or pathclean.startswith(args.folder[0]+'\\'))
	  and (args.subfolders or (pathclean.find('/') == -1 and pathclean.find('\\') == -1) or (args.folder != None and pathclean.find('/', len(args.folder[0]) + 1) == -1 and pathclean.find('\\', len(args.folder[0]) + 1) == -1))
	  and (args.favonly == False or game.findtext('favorite') == 'true')
	  and (args.checkfiles == False or os.path.exists(path))
	  and (args.includehidden or game.findtext('hidden') != 'true')):
		item = {
			'path': '',
			'label': name,
			'core_path': 'DETECT',
			'core_name': 'DETECT',
			'crc32': 'DETECT'
		}
		if basepath != None:
			if basepath[:1] == '/':
				item['path'] = basepath + pathclean.replace('\\', '/')
			else:
				item['path'] = basepath + pathclean.replace('/', '\\')
		else:
			item['path'] = os.path.abspath(path)
		if args.dbname != None:
			item['db_name'] = args.dbname[0]
		if (args.crc32 and os.path.isfile(path)):
			with open(path, 'rb') as handle:
				crc = 0
				while (block := handle.read(1048576)):
					crc = zlib.crc32(block, crc)
				item['crc32'] = "{0:08X}|crc".format(crc)
		result['items'].append(item)
		if args.copypics != None:
			pic = game.findtext(args.copypics[0])
			if pic != None:
				pic = os.path.normpath(pic.encode('Latin-1').decode('utf-8'))
				picdst = os.path.join(args.copypics[1], name.encode('Latin-1').decode('utf-8').replace('&','_').replace('*','_').replace('/','_').replace(':','_').replace('`','_').replace('<','_').replace('>','_').replace('?','_').replace('\\','_').replace('|','_')+os.path.splitext(pic)[1])
				if (not os.path.exists(picdst)):
					shutil.copy(pic, picdst)

if len(result['items']) > 0:
	json.dump(result, args.outfile, indent = '  ', ensure_ascii = False)
else:
	args.outfile.close()
	os.remove(args.outfile.name)
print("{} game(s) converted.".format(len(result['items'])))
