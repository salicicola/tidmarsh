<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />

<xsl:template name="calendar_page">
   <div id="calendar_page">
        <xsl:if test="not ($page='calendar_page')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
        <div style="margin-left:1.5em;padding-right:1em;font-weight:normal;font-size:90%">
		2017 wall calendar produced by Salicicola features a few carnivorous plants that occur in eastern Massachusetts. 
        </div>
       <iframe style="margin:0;padding:0;border:0" width="650" scrolling="no"  height="730"  frameborder="0" 
src="/servlet/SaxonServletX?source=/calendar/stub.xml&amp;style=/calendar/calendar.xsl&amp;clear-stylesheet-cache=yes"></iframe> 
   </div>
</xsl:template>

</xsl:stylesheet>
