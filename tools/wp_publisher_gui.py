#!/usr/bin/env python3
"""
wp_publisher_gui.py

Tkinter desktop GUI for publishing to WordPress without touching the terminal.

Install: pip install requests
Run:     python3 tools/wp_publisher_gui.py

Credentials via environment variables: WP_API_URL, WP_PLUGIN_KEY
"""

import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

try:
    import requests
except ImportError:
    print('Run: pip install requests')
    exit(1)

WP_URL = os.environ.get('WP_API_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY = os.environ.get('WP_PLUGIN_KEY', '')

CATEGORIES = [
    'ELT Masterclass', 'Grammar', 'Listening & Phonology', 'Speaking',
    'Reading', 'Writing', 'Vocabulary', 'CELTA', 'Uncategorized'
]

KEYWORD_TAGS = {
    'grammar': 'grammar', 'tense': 'tense', 'verb': 'verb',
    'listen': 'listening', 'pronunciation': 'pronunciation', 'phonetic': 'phonetics',
    'speak': 'speaking', 'fluency': 'fluency', 'conversation': 'conversation',
    'read': 'reading', 'comprehension': 'comprehension',
    'writ': 'writing', 'essay': 'essay',
    'vocabulary': 'vocabulary', 'idiom': 'idiom', 'phrasal': 'phrasal verb',
    'celta': 'CELTA', 'lesson': 'lesson plan'
}


def suggest_tags(text):
    t = text.lower()
    return [tag for kw, tag in KEYWORD_TAGS.items() if kw in t]


def publish(api_url, api_key, payload, callback):
    try:
        resp = requests.post(
            api_url, json=payload,
            headers={'X-Sourov-Key': api_key},
            timeout=30
        )
        resp.raise_for_status()
        callback(True, resp.json())
    except Exception as e:
        callback(False, str(e))


class PublisherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('WP Publisher')
        self.geometry('700x640')
        self.configure(bg='#1e1e1e')
        self.resizable(True, True)
        self._build_ui()

    def _build_ui(self):
        bg  = '#1e1e1e'
        sbg = '#252526'
        fg  = '#d4d4d4'
        acc = '#0e639c'
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground=sbg, background=sbg,
                        foreground=fg, arrowcolor=fg)

        def label(parent, text):
            return tk.Label(parent, text=text, bg=bg, fg='#858585',
                            font=('Segoe UI', 9))

        def entry(parent, **kw):
            return tk.Entry(parent, bg=sbg, fg=fg, insertbackground=fg,
                            relief='flat', font=('Segoe UI', 11), **kw)

        pad = dict(padx=12, pady=4, sticky='ew')
        self.columnconfigure(0, weight=1)

        label(self, 'Post Title').grid(row=0, column=0, padx=12, pady=(12,0), sticky='w')
        self.e_title = entry(self)
        self.e_title.grid(row=1, column=0, **pad)
        self.e_title.bind('<KeyRelease>', self._auto_suggest)

        label(self, 'Content (HTML allowed)').grid(row=2, column=0, padx=12, pady=(8,0), sticky='w')
        self.t_content = scrolledtext.ScrolledText(
            self, height=12, bg=sbg, fg=fg, insertbackground=fg,
            relief='flat', font=('Segoe UI', 11), wrap='word'
        )
        self.t_content.grid(row=3, column=0, **pad)

        fr = tk.Frame(self, bg=bg)
        fr.grid(row=4, column=0, **pad)
        fr.columnconfigure(0, weight=1)
        fr.columnconfigure(1, weight=2)

        label(fr, 'Category').grid(row=0, column=0, sticky='w', padx=(0,8))
        self.combo_cat = ttk.Combobox(fr, values=CATEGORIES, state='readonly', width=22)
        self.combo_cat.set('ELT Masterclass')
        self.combo_cat.grid(row=1, column=0, sticky='ew', padx=(0,12))

        label(fr, 'Tags (comma-separated)').grid(row=0, column=1, sticky='w')
        self.e_tags = entry(fr)
        self.e_tags.grid(row=1, column=1, sticky='ew')

        fr2 = tk.Frame(self, bg=bg)
        fr2.grid(row=5, column=0, **pad)
        fr2.columnconfigure(0, weight=1)
        fr2.columnconfigure(1, weight=1)

        label(fr2, 'SEO Title (60 chars max)').grid(row=0, column=0, sticky='w', padx=(0,8))
        self.e_seo = entry(fr2)
        self.e_seo.grid(row=1, column=0, sticky='ew', padx=(0,12))

        label(fr2, 'Meta Description (155 chars)').grid(row=0, column=1, sticky='w')
        self.e_meta = entry(fr2)
        self.e_meta.grid(row=1, column=1, sticky='ew')

        self.var_status = tk.StringVar(value='draft')
        fr3 = tk.Frame(self, bg=bg)
        fr3.grid(row=6, column=0, **pad)
        for val, txt in [('draft','Save as Draft'), ('publish','Publish Now'), ('future','Schedule')]:
            tk.Radiobutton(fr3, text=txt, variable=self.var_status, value=val,
                           bg=bg, fg=fg, selectcolor=sbg,
                           activebackground=bg, activeforeground=fg).pack(side='left', padx=8)

        self.e_date = entry(self)
        self.e_date.insert(0, 'Schedule: YYYY-MM-DDTHH:MM:SS (leave blank for draft)')
        self.e_date.grid(row=7, column=0, **pad)

        fr4 = tk.Frame(self, bg=bg)
        fr4.grid(row=8, column=0, **pad)
        fr4.columnconfigure(0, weight=1)
        fr4.columnconfigure(1, weight=1)
        label(fr4, 'WordPress API URL').grid(row=0, column=0, sticky='w')
        self.e_url = entry(fr4)
        self.e_url.insert(0, WP_URL)
        self.e_url.grid(row=1, column=0, sticky='ew', padx=(0,8))
        label(fr4, 'Plugin Secret Key').grid(row=0, column=1, sticky='w')
        self.e_key = entry(fr4, show='*')
        self.e_key.insert(0, WP_KEY)
        self.e_key.grid(row=1, column=1, sticky='ew')

        self.btn = tk.Button(
            self, text='Publish to WordPress',
            command=self._do_publish,
            bg=acc, fg='white', relief='flat',
            font=('Segoe UI', 11, 'bold'),
            padx=20, pady=8, cursor='hand2'
        )
        self.btn.grid(row=9, column=0, pady=12)

        self.lbl_status = tk.Label(self, text='Ready', bg=bg, fg='#858585',
                                   font=('Segoe UI', 9))
        self.lbl_status.grid(row=10, column=0, pady=(0,8))

    def _auto_suggest(self, _event=None):
        title = self.e_title.get()
        if not self.e_seo.get() or self.e_seo.get() == self.e_title.get():
            self.e_seo.delete(0, 'end')
            self.e_seo.insert(0, title[:60])
        tags = suggest_tags(title)
        if tags and not self.e_tags.get():
            self.e_tags.delete(0, 'end')
            self.e_tags.insert(0, ', '.join(tags))

    def _do_publish(self):
        title   = self.e_title.get().strip()
        content = self.t_content.get('1.0', 'end').strip()
        if not title or not content:
            messagebox.showwarning('Missing fields', 'Title and Content are required.')
            return

        status = self.var_status.get()
        date   = self.e_date.get().strip()
        if 'Schedule:' in date:
            date = ''

        payload = {
            'title':            title,
            'content':          content,
            'category':         self.combo_cat.get(),
            'tags':             self.e_tags.get(),
            'status':           'future' if date else status,
            'seo_title':        self.e_seo.get()[:60],
            'meta_description': self.e_meta.get()[:155],
        }
        if date:
            payload['date'] = date

        url = self.e_url.get().strip()
        key = self.e_key.get().strip()
        if not key:
            messagebox.showerror('Missing key', 'Enter your Plugin Secret Key.')
            return

        self.btn.configure(state='disabled', text='Publishing...')
        self.lbl_status.configure(text='Connecting to WordPress...', fg='#dcdcaa')

        threading.Thread(
            target=publish,
            args=(url, key, payload, self._on_result),
            daemon=True
        ).start()

    def _on_result(self, success, data):
        self.after(0, self._update_ui, success, data)

    def _update_ui(self, success, data):
        self.btn.configure(state='normal', text='Publish to WordPress')
        if success:
            post_id = data.get('post_id', data.get('id', '?'))
            self.lbl_status.configure(text=f'Published! Post ID: {post_id}', fg='#4ec9b0')
            messagebox.showinfo('Success', f'Post created!\nID: {post_id}')
            self.e_title.delete(0, 'end')
            self.t_content.delete('1.0', 'end')
            self.e_tags.delete(0, 'end')
            self.e_seo.delete(0, 'end')
            self.e_meta.delete(0, 'end')
        else:
            self.lbl_status.configure(text=f'Error: {data}', fg='#f44747')
            messagebox.showerror('Error', str(data))


if __name__ == '__main__':
    app = PublisherApp()
    app.mainloop()
