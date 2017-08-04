#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.sax

class nodeHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.CurrentData = ""
      self.focusable = ""
      self.checkable = ""
      self.year = ""
      self.rating = ""
      self.stars = ""
      self.description = ""

   # 元素开始事件处理
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "node":
         print "*****node*****"
         text = attributes["text"]
         print "text:", text

   # 元素结束事件处理
   def endElement(self, tag):
      if self.CurrentData == "focusable":
         print "focusable:", self.focusable
      elif self.CurrentData == "checkable":
         print "checkable:", self.checkable

   # 内容事件处理
   def characters(self, content):
      if self.CurrentData == "focusable":
         self.focusable = content
      elif self.CurrentData == "checkable":
         self.checkable = content
  
if ( __name__ == "__main__"):
   
   # 创建一个 XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # 重写 ContextHandler
   Handler = nodeHandler()
   parser.setContentHandler( Handler )
   
   parser.parse("hierarchy.xml")