<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
  <xsl:output method="xml" indent="no" omit-xml-declaration="yes" />
  <xsl:template name="events">
	  <div id="events">
		<xsl:if test="not ($page='events')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
		<div style="float:right;margin-left:10px;">
			<img align="right" alt="" 
			title="" 
			width="300" border="1" onclick="openImage(this)" 
			src="/static/photos/201509/20150920olymp7117a.jpg"/> 
		</div>
		<div class="header">
			<h2>Salicicola Past Events<br/>
				<span style="font-size:80%;font-weight:normal">Presentations, workshops, walks</span>
			</h2>
		</div>
	
		<xsl:for-each select="//events/event">
		<div class="section">
			<xsl:choose>
				<xsl:when test="@href">
					<div class="section_header"><a href="{@href}"><xsl:value-of select="@name"/></a></div>
				</xsl:when>
				<xsl:otherwise>
					<div class="section_header"><xsl:value-of select="@name"/></div>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:for-each  select="page">
				<div class="item"><a href="{@href}"><xsl:value-of select="@name|."/></a></div>
			</xsl:for-each>		 	
				<div style="text-indent:-2ex;padding-left:4ex"><br/></div> 
				<!-- FIXME since there are so few of them, yet -->
		</div>
		</xsl:for-each>
	   </div>
</xsl:template>
</xsl:stylesheet>
