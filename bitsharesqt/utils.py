from PyQt5 import QtGui, QtCore

COLOR_GREEN = "#27ca41"
COLOR_RED = "#e44842"

def ignore_hidpi_settings():
    font = app().font()
    font.setPixelSize(12)
    app().setFont(font)

from pytimeparse.timeparse import timeparse
def deltasec(tp, default=3600*24):
	if not tp or len(tp) < 1:
		return default
	return timeparse(tp)
def deltainterval(s):
	edges = [ ("s", 1), ("m", 60), ("h", 60), (" day", 24),
		(" week", 7), (" month", 4), (" year", 12),]
	unit = "s"
	for remark, div in edges:
		n = s / div
		if n < 1:
			break
		s = n ; unit = remark
	suf = "s" if (s > 1 and len(unit) > 1) else ""
	return "%0.f%s%s" % (s, unit, suf)

def neatbytes(nb):
	kb = nb / 1024
	mb = kb / 1024
	gb = mb / 1024
	if gb >= 1:
		return "{:.2f} GB".format(gb)
	if mb >= 1:
		return "{:.2f} MB".format(mb)
	if kb >= 1:
		return "{:.2f} KB".format(kb)
	return "{} bytes".format(nb)

def generate_webwalletlike_password():
	from bitsharesbase.account import PrivateKey
	random_private_key_asWif = repr(PrivateKey(wif=None))
	return ("P" + random_private_key_asWif) [0:45]

def app():
	return QtGui.QApplication.instance()

def rootwin(widget):
	n = widget
	while n:
		p = widget.parent()
		if p: n = p
		else: break
	return n

def qclip(text=None):
	clipboard = QtGui.QApplication.clipboard()
	if text is None: # get
		return clipboard.text()
	else: # set
		clipboard.setText(text)

def num_args(method):
	all_args = method.__code__.co_argcount
	num_kwargs = len(method.__defaults__) if method.__defaults__ else 0
	return all_args - num_kwargs

def safeslot(func):
	def wrapper(*args, **kwargs):
		try:
			args = args[0:num_args(func)]
			return func(*args, **kwargs)
		except Exception as e:
			showexc(e)
	return wrapper



def anyvalvis(widget, default):
	if widget.isVisible():
		return any_value(widget)
	return default

def any_value(widget):
	if isinstance(widget, QtGui.QComboBox):
		return widget.currentText()
	if isinstance(widget, QtGui.QLineEdit):
		return widget.text()
	if isinstance(widget, QtGui.QSpinBox):
		return widget.value()
	if isinstance(widget, QtGui.QDoubleSpinBox):
		return widget.value()
	if isinstance(widget, QtGui.QCheckBox):
		return widget.checked()

def any_change(widget, func, progress=None):
	if isinstance(widget, QtGui.QComboBox):
		return on_combo(widget, func)
	if isinstance(widget, QtGui.QLineEdit):
		return on_edit(widget, func, progress)
	if isinstance(widget, QtGui.QSpinBox):
		return on_spin(widget, func)
	if isinstance(widget, QtGui.QDoubleSpinBox):
		return on_spin(widget, func)
	if isinstance(widget, QtGui.QCheckBox):
		return on_state(widget, func)


def set_value(widget, val):
	if isinstance(widget, QtGui.QComboBox):
		set_combo(widget, val)
	if isinstance(widget, QtGui.QLineEdit):
		widget.setText(str(val))
	if isinstance(widget, QtGui.QSpinBox):
		widget.setValue(val)
	if isinstance(widget, QtGui.QDoubleSpinBox):
		widget.setValue(val)
	if isinstance(widget, QtGui.QCheckBox):
		widget.setChecked(bool(val))


import traceback
def showexc(e, echo=False):
	if echo or True:
		traceback.print_exc()
	showerror(e.__class__.__name__ + ' | ' + str(e), additional=e.__class__.__doc__)

def showmb(message, title="Information", additional=None, details=None, min_width=None, icon=None):
	msg = QtGui.QMessageBox()
	msg.setIcon( QtGui.QMessageBox.Information )
	
	msg.setText(message)
	msg.setWindowTitle(title)
	msg.setWindowIcon(app().mainwin.windowIcon())
	
	if min_width:
		msg.setStyleSheet("QLabel{min-width: "+str(min_width)+"px;}")
		msg.setIcon(QtGui.QMessageBox.NoIcon)
	
	if icon == "error":
		msg.setIcon( QtGui.QMessageBox.Critical )
	elif icon == "warning":
		msg.setIcon( QtGui.QMessageBox.Warning )
	elif icon:
		msg.setIconPixmap(QtGui.QPixmap(icon))
	
	if additional:
		msg.setInformativeText(str(additional))
	
	if details:
		msg.setDetailedText(details)
	
	msg.setStandardButtons( QtGui.QMessageBox.Ok )
	
	retval = msg.exec_()
	return retval


def showwarning(message, title="Warning", additional=None, details=None):
	return showmb(message, title, additional, details, icon="warning")

def showerror(message, title="Error", additional=None, details=None):
	return showmb(message, title, additional, details, icon="error")

def showdialog(message, title="Information", additional=None, details=None, min_width=None, icon=None):
	return showmb(message, title, additional, details, min_width, icon)

# Aliases:
def showmessage(*args, **kwargs):
	return showdialog(*args, **kwargs)
def showmsg(*args, **kwargs):
	return showdialog(*args, **kwargs)
def showwarn(*args, **kwargs):
	return showwarning(*args, **kwargs)
def showerr(*args, **kwargs):
	return showerror(*args, **kwargs)


def askyesno(message):
	#mb = QtGui.QMessageBox
	#if mb.question(None, '', message,
	#	mb.Yes | mb.No, mb.No) == mb.Yes:
	#	return True
	#return False
	msg = QtGui.QMessageBox()
	msg.setIcon( QtGui.QMessageBox.Question )
	
	msg.setText(message)
	#msg.setWindowTitle(title)
	msg.setWindowIcon(app().mainwin.windowIcon())
	
	msg.setStandardButtons( QtGui.QMessageBox.Yes | QtGui.QMessageBox.No )
	retval = msg.exec_()
	return bool(retval == QtGui.QMessageBox.Yes)

def qmenu(elem, func):
	elem.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
	elem.customContextMenuRequested.connect(func)

def qmenu_exec(elem, menu, position):
	return menu.exec_(elem.viewport().mapToGlobal(position))

def qaction(qttr, menu, text, func):
	act = QtGui.QAction(qttr.tr(text), menu)
	act.triggered.connect(func)
	#newAct->setShortcuts(QKeySequence::New)
	#newAct->setStatusTip(tr("Create a new file"))
	menu.addAction(act)
	return act

def qtimer(delay, cb):
	timer = QtCore.QTimer()
	timer.start(delay)
	timer.timeout.connect(cb)
	return timer

def picon(path):
	ico = QtGui.QPixmap(path)
	return ico

def licon(path):
	ico = QtGui.QPixmap(path)
	img = QtGui.QLabel("")
	img.setPixmap(ico)
	return img

def qicon(path):
	ico = QtGui.QPixmap(path)
	icon = QtGui.QIcon(ico)
	return icon


def fill_combo(combo, options):
	combo.clear()
	for option in options:
		combo.addItem(option)

def sync_combo(combo, options):
	for option in options:
		if combo.findText(option, QtCore.Qt.MatchFixedString) >= 0:
			continue
		combo.addItem(option)


def set_combo(combo, text, force=False, icon=None):
	index = combo.findText(text, QtCore.Qt.MatchFixedString)
	if index >= 0:
		combo.setCurrentIndex(index)
	elif force:
		if icon:
			combo.addItem(icon, text)
		else:
			combo.addItem(text)
		set_combo(combo, text, False)
	elif combo.lineEdit():
		combo.lineEdit().setText(text)
	else:
		print("Unable to set", text, "on", combo)

def on_combo(combo, func, progress=True):
	if combo.lineEdit():
		on_edit(combo.lineEdit(), func, progress)
	elif progress is True:
		combo.editTextChanged.connect(func)
	combo.currentIndexChanged.connect(func)
def on_spin(spin, func):
	spin.valueChanged.connect(func)
def on_edit(line, func, progress=True):
	if progress is True:
		line.textChanged.connect(func)
	if progress is False:
		line.editingFinished.connect(func)
def on_check(box, func):
	box.stateChanged.connect(func)

def add_item(widget, value, icon=None):
	if isinstance(widget, QtGui.QListWidget):
		item = QtGui.QListWidgetItem(str(value))
		item.setIcon(icon)
		widget.addItem(item)
	elif isinstance(widget, QtGui.QComboBox):
		if icon:
			widget.addItem(icon, value)
		else:
			widget.addItem(value)
	else:
		print("Unable to add item", value, "on", widget)

def set_itemflags(item, enabled=True, checked=False, checkable=False, selectable=True):
	o = 0
	if checked:
		checkable = True
	if selectable:
		o |= QtCore.Qt.ItemIsSelectable
	if enabled:
		o |= QtCore.Qt.ItemIsEnabled
	if checkable:
		o |= QtCore.Qt.ItemIsUserCheckable
	if checked:
		o |= QtCore.Qt.ItemIsChecked
	item.blockSignals(True)
	item.setFlags(o)
	item.blockSignals(False)

def table_selrow(table):
	indexes = table.selectionModel().selectedRows()
	if len(indexes) < 1:
		return -1
	j = indexes[0].row()
	return j

def table_coldata(table, row, col):
	return table.item(row, col).data(99)

from PyQt5.QtWidgets import QTableWidgetItem
def set_col(table, row, col, val, fmt=None, color=None, align=None, editable=None, data=None, icon=None):
	item = QTableWidgetItem(fmt % val if fmt else str(val))
	if color:
		item.setForeground(QtGui.QColor(color))
	if align=="right":
		item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
	if align=="center":
		item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
	if not(editable is None):
		if editable:
			item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
				| QtCore.Qt.ItemIsEditable)
		else:
			item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
	if data:
		item.setData(99, data)
	if icon:
		item.setIcon(icon)
	
	table.setItem(row, col, item)
	return item


def stretch_table(table, col=None, hidehoriz=False):
	table.verticalHeader().hide()
	
	header = table.horizontalHeader()
	n = header.count()
	if col is None:
		col = n - 1
	for i in range(0, n):
		header.setResizeMode(i, QtGui.QHeaderView.ResizeToContents)
	if not(col is False):
		header.setResizeMode(col, QtGui.QHeaderView.Stretch)
	if hidehoriz:
		header.hide()

def stretch_tree(tree):
	header = tree.header()
	header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
	#_treeWidget->header()->setStretchLastSection(false)
	#_treeWidget->header()->setSectionResizeMode(QHeaderView::ResizeToContents)
	#header.setResizeMode(1, QtGui.QHeaderView.Stretch)
	#table.verticalHeader().hide()

def merge_in(root, obj, key="", label=None, iso=None):
	
	item = QtGui.QTreeWidgetItem(root)
	
	item.setText(0, key)
	item.setText(1, str(obj))
	#print(obj, str(obj))
	if label:
		item.setText(1, label)
	
	nextlabel = None
	
	if type(obj) == str or type(obj) == int or type(obj) == float or type(obj) == bool:
		return
	elif type(obj) == dict:
		op_obj = obj
	elif type(obj) == list:
		pass
	elif obj is None:
		return
	else:
		op_obj = obj.json()
	
	if type(obj) == list:
		for key, val in enumerate(obj):
			merge_in(item, val, str(key), nextlabel, iso=iso)
		return
	
	for key in op_obj:
		#from pprint import pprint
		#print("Trying to merge in:", op_obj, key)
		val = op_obj[key]
		merge_in(item, val, key+": ", nextlabel, iso=iso)

def dict_compare(d1, d2):
	d1_keys = set(d1.keys())
	d2_keys = set(d2.keys())
	intersect_keys = d1_keys.intersection(d2_keys)
	added = d1_keys - d2_keys
	removed = d2_keys - d1_keys
	def cmpval(d1, d2, o):
		if isinstance(d1[o], dict) and isinstance(d2[o], dict):
			return dict_same(d1[o], d2[o])
		return d1[o] == d2[o]
	modified = {o : (d1[o], d2[o]) for o in intersect_keys if not(cmpval(d1, d2, o))}
	same = set(o for o in intersect_keys if cmpval(d1,d2,o))
	return added, removed, modified, same

def dict_same(d1, d2):
	added, removed, modified, same = dict_compare(d1, d2)
	#print("added", added, "removed:", removed, "modified:", modified)
	return not(bool(len(added) + len(removed) + len(modified)))


import qrcode
class QQRPainter(qrcode.image.base.BaseImage):
	def __init__(self, border, width, box_size):
		self.border = border
		self.width = width
		self.box_size = box_size
		size = (width + border * 2) * box_size
		self._image = QtGui.QImage(
			size, size, QtGui.QImage.Format_RGB16)
		self._image.fill(QtCore.Qt.white)

	def pixmap(self):
		return QtGui.QPixmap.fromImage(self._image)

	def drawrect(self, row, col):
		painter = QtGui.QPainter(self._image)
		painter.fillRect(
			(col + self.border) * self.box_size,
			(row + self.border) * self.box_size,
			self.box_size, self.box_size,
		QtCore.Qt.black)

	def save(self, stream, kind=None):
		pass

def make_qrcode_image(text):
	bs = 6
	if len(text) >= 60:
		bs = 5
	if len(text) >= 100:
		bs = 4
	return qrcode.make(text, box_size=bs, border=2, image_factory=QQRPainter)


class StackLinker(QtCore.QObject):
	def __init__(self, stack, buttons, pre_highlight, parent=None):
		super(StackLinker, self).__init__(parent)
		self.stack = stack
		self.buttons = [ ]
		self.wr = pre_highlight
		self._index = stack.currentIndex()
		for btn in buttons:
			self.addEntry(*btn)
		self.highlightButtons()
	
	def addEntry(self, btn, qact, tag):
		btn._tag = tag
		btn._index = len(self.buttons)
		self.buttons.append( btn )
		btn.clicked.connect(self.on_button_click)
		
		qact.triggered.connect(self.on_action_trigger)
		qact._index = btn._index
	
	def on_action_trigger(self):
		qact = self.sender()
		self.wr()
		self.setPage(qact._index)
		return False
	
	def on_button_click(self):
		btn = self.sender()
		self.setPage(btn._index)
		return False
	
	def highlightButtons(self):
		for btn in self.buttons:
			if btn._index == self._index:
				btn.setChecked(True)
			else:
				btn.setChecked(False)
	
	def setPageByTag(self, tag):
		i = -1
		for btn in self.buttons:
			i += 1
			if (btn._tag == tag):
				self.setPage(i)
				break
	
	def setPage(self, ind):
		self._index = ind
		self.stack.setCurrentIndex(ind)
		self._index = self.stack.currentIndex()
		self.highlightButtons()

from PyQt5.QtGui import QTextCursor
class ScrollKeeper():
	def __init__(self, elem, cursor=False):
		self.elem = elem
		self.vs = elem.verticalScrollBar()
		self.cursor = cursor
		
	def __enter__(self):
		max_ = self.vs.maximum()
		self.old_val = self.vs.value()
		self.at_bottom = (self.old_val == max_)
		if not(max_): self.at_bottom = True
		if self.cursor:
			tc = self.elem.textCursor()
			tc.movePosition(QTextCursor.End)
			self.old_tc = tc
		return self
		
	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.at_bottom:
			val = self.vs.maximum()
		else:
			val = self.old_val
		self.vs.setValue(val)
		if self.cursor:
			self.elem.setTextCursor(self.old_tc)


from logging import Handler
class ConsoleLogger(Handler):
	def emit(self, record):
		msg = record.getMessage()
		print(msg) # good old stdout
		app().mainwin.log_record.emit(record)

import re
def linksInText(s, black_list=[ "download", "save" ]):
	r = [ ]
	possible = re.findall("([a-z0-9]+):(.+?)($|\s|\"|\')", s)
	for (scheme, path, end) in possible:
		if scheme in black_list:
			continue
		full = scheme + ":" + path
		r.append(full)
	return r

from collections import namedtuple
ParseResult = namedtuple('ParseResult', ['scheme', 'netloc', 'path', 'params',
			'query', 'fragment', 'username', 'password', 'hostname',
			'port'])
import urllib.parse
def parseUrl(url):
	r = urllib.parse.urlparse(url, scheme='', allow_fragments=True)
	params = urllib.parse.parse_qs(r.query, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace'),
	data = { }
	for d in params:
		for k, v in d.items():
			if len(v) == 1: v = v[0]
			data[k] = v
	return ParseResult(
		r.scheme,
		r.netloc,
		r.path,
		data,
		r.query,
		r.fragment,
		r.username,
		r.password,
		r.hostname,
		r.port
	)

from bitsharesbase.operations import getOperationNameForId
from bitshares.asset import Asset
from bitshares.amount import Amount
def parseBTSUrl(url, bitshares_instance=None, expand=False):
	scheme, url = url.split(":", 1)
	if not "?" in url:
		path = url
		params = ""
	else:
		path, params = url.split("?", 1)
		params = urllib.parse.unquote(params)
		if not "&" in params:
			params = [ params ]
		else:
			params = params.split("&")
	data = { }
	def cnv_value(v):
		try:
			return int(v)
		except:
			try:
				return float(v)
			except:
				pass
		return v
	def set_key(b, k, v):
		p = re.match('^\[(.*?)\](.*)', k)
		if p:
			bk = p.group(1)
			mk = ""
			rest = p.group(2)
			if (bk and isinstance(b, list)):
				for sub in b:
					if not(isinstance(sub, dict)):
						break
					if not(bk in sub):
						set_key(sub, bk + rest, v)
						return
			if not(bk) and isinstance(b, list) and len(b) > 0:
				set_key(b[-1], rest, v)
			elif not(bk in b):
				if len(bk) < 1:
					cnt = [ ]
				else:
					cnt = { }
				if isinstance(b, list):
					b.append(cnt)
				else:
					b[bk] = cnt
				set_key(cnt, bk+rest, v)
			return

		p = re.match('^(.+?)\[(.*?)\](.*)', k)
		if p:
			bk = p.group(1)
			mk = p.group(2)
			rest = p.group(3)
			if not(bk in b):
				if len(mk) < 1:
					b[bk] = [ ]
				else:
					b[bk] = { }
			set_key(b[bk], mk+rest, v)
			return

		v = cnv_value(v)
		if isinstance(b, list) and not k:
			b.append(v)
		else:
			b[k] = v
		return

	for p in params:
		k, v = p.split("=")
		#data[k] = v
		set_key(data, k, v)

	action = path.split("/")
	if action[0] == "op": action[0] = "operation"
	if action[0] == "bl": action[0] = "block"
	if action[0] == "trx": action[0] = "transaction"
	if action[0] == "ob": action[0] = "object"

	if action[0] == "block":
		if len(action) > 1: data["block_num"]    = int(action[1])
		if len(action) > 2: data["trx_in_block"] = int(action[2])
		if len(action) > 3: data["op_in_trx"]    = int(action[3])
		if len(action) > 4: data["virtual_op"]   = int(action[4])
	if action[0] == "operation":
		try:
			action[1] = getOperationNameForId(int(action[1]))
		except:
			pass
		if bitshares_instance and expand:
			try:
				if "asset" in data and "amount" in data:# and not(isinstance(data["amount"], dict)):
					asset = Asset(data["asset"], blockchain_instance=bitshares_instance)
					asset_id = asset["id"]
					amount = Amount(data["amount"], asset_id, blockchain_instance=bitshares_instance)
					data.pop("asset")
					data.pop("amount")
					set_key(data, "amount[asset_id]", asset_id)
					set_key(data, "amount[amount]", int(amount))
				elif "asset" in data:
					asset = Asset(data["asset"], blockchain_instance=bitshares_instance)
					data.pop("asset")
					set_key(data, "amount[asset_id]", asset["id"])
			except:
				import traceback
				traceback.print_exc()
				pass

	return {
		'scheme': scheme,
		'path': path,
		'action': action, #path.split("/"),
		'params': data
	}
