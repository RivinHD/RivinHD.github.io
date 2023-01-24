#!/usr/bin/env python

'''
tag_generator.py

Copyright 2017 Long Qian
Contact: lqian8@jhu.edu

This script creates tags for your Jekyll blog hosted by Github page.
No plugins required.
'''

import glob
import os

check_dirs = ('_posts/', '_drafts/', '_blender-addons/')
tag_dir = 'tag_archive/'

def get_tags(check_dirs, verbose=True):
    '''
    Adapted from tag_generator.py
    Copyright 2017 Long Qian
    Contact: lqian8@jhu.edu
    This script created tags for a Jekyll blog hosted by Github page.
    No plugins required.
    See https://longqian.me/2017/02/09/github-jekyll-tag/
    
    Updated 2019-12-05
    Arturo Moncada-Torres
    arturomoncadatorres@gmail.com
    Adapted script to process .md files with tags in format
    tags:
        - tag1
        - tag2
        ...
    Notice that for this to work properly, tags must be the last element of the
    Markdown header.
    
    Parameters
    ----------
    post_dir: string
        Path to directory _posts/
        
    verbose: boolean
        Indicate if status messages are printed (True) or not (False)
    Returns
    -------
    total_tags: set
        Set with all the tags used in the different posts.
    '''    
    
    # Get Markdown files.
    filenames = []
    for dir in check_dirs:
        filenames.extend(glob.glob(dir + '*md'))
    
    # Loop through all files.
    total_tags = []
    for filename in filenames:
        f = open(filename, 'r', encoding='utf8')
        crawl = False
        tag_lines_coming = False
        for line in f.readlines():
            current_line = line.strip()
            if crawl:
                if current_line == 'tags:':
                    tag_lines_coming = True
                    continue
                    
            if not current_line.startswith('-'):
                tag_lines_coming = False
                    
            # If --- delimiter is found, start crawling.
            if current_line == '---':
                if not crawl:
                    crawl = True
                else:
                    crawl = False
                    break
                
            # If we are in the actual tag lines (that is, tag_lines_coming is
            # True and we aren't in the tags: line), extract them.
            if tag_lines_coming and (current_line != 'tags:'):
                total_tags.append(current_line.strip('- '))
        f.close()
        
    # Make tags unique in a set.
    total_tags = set(total_tags)
    
    if verbose:
        print("Found " + str(total_tags.__len__()) + " tags")
    
    return total_tags


#%%
def create_tags_posts(tag_dir, total_tags=set(), verbose=True):
    '''
    Adapted from tag_generator.py
    Copyright 2017 Long Qian
    Contact: lqian8@jhu.edu
    This script created tag posts for a Jekyll blog hosted by Github page.
    No plugins required.
    See https://longqian.me/2017/02/09/github-jekyll-tag/
    
    Updated 2019-12-11
    Arturo Moncada-Torres
    arturomoncadatorres@gmail.com
    Modularized for ease of use in update_tags.py.
    
    Parameters
    ----------
    post_dir: string
        Path to directory directory where tag posts will be created.
        
    total_tags: set
        
        
    verbose: boolean
        Indicate if status messages are printed (True) or not (False)
    Returns
    -------
    None
    '''
    
    if total_tags.__len__() == 0:
        print("No tags. Thus, no tag posts were created")
        return None
    
    else:
    
        old_tags = glob.glob(tag_dir + '*.md')
        for tag in old_tags:
            os.remove(tag)
            
        if not os.path.exists(tag_dir):
            os.makedirs(tag_dir)
        
        for tag in total_tags:
            tag_filename = tag_dir + tag + '.md'
            f = open(tag_filename, 'a')
            write_str = '---\nlayout: tag_page\ntitle: \"Tag: ' + tag + '\"\ntag: ' + tag + '\nrobots: noindex\n---\n'
            f.write(write_str)
            f.close()
            
        if verbose:
            print("Created " + str(total_tags.__len__()) + " tag posts")
            
        return None
    
if __name__ == '__main__':
    tags = get_tags(check_dirs)
    print(tags)
    create_tags_posts(tag_dir, tags)
