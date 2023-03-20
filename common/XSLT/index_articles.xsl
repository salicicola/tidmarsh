<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />

<xsl:template name="articles">
   <div id="articles">
        <xsl:if test="not ($page='articles')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div style="float:right;margin-left:10px;">
<img alt="Courtesy of Oleg Korsun (http://www.nature.chita.ru)" 
title="Courtesy of Oleg Korsun (http://www.nature.chita.ru)" 
src="/static/slides/chosenia_arbutifolia3.jpg" align="right" border="1" width="300"/>
	</div>
	<div class="header">
		<h2>Articles &amp; Short Notes</h2>
	</div>	
	<div class="items">
		<ul style="margin-top:0">
		<li style="margin-left:-2ex">
			<b>Willows</b> (<span style="cursor:pointer" onmouseover="this.style.color='red'" onmouseout="this.style.color='{$color}'" onclick="switch_display(this.parentNode, 'div')">hide/show</span>)	
			<xsl:for-each select="//articles/article[position() &lt; 9]">
				<div class="item" style="display:none">
				<a href="http://172.104.19.75{@href}"><xsl:copy-of select="* | text()"/>&#160;
                      		<!--<br/>&#8212;--> 
                      		<span style="white-space:nowrap">
                      		<i><xsl:value-of select="@authors"/><xsl:text> </xsl:text><xsl:value-of select="@year"/></i></span></a>
				</div>
			</xsl:for-each>
			</li>
			<li style="margin-left:-2ex">
				<b>Chosenia</b> (<span style="cursor:pointer" onmouseover="this.style.color='red'" onmouseout="this.style.color='{$color}'"  onclick="switch_display(this.parentNode, 'div')">hide/show</span>)
		<xsl:for-each select="//articles/article[position() &gt; 8]">
				<div class="item" style="display:none">
					<a href="http://172.104.19.75{@href}"><xsl:copy-of select="* | text()"/>&#160; <span style="white-space:nowrap">
							<i><xsl:value-of select="@authors"/><xsl:text> </xsl:text><xsl:value-of select="@year"/></i>
			</span></a></div>
		</xsl:for-each>
		</li>
		<li style="margin-left:-2ex">
			<b>Other</b> (<span style="cursor:pointer" onmouseover="this.style.color='red'" onmouseout="this.style.color='{$color}'" onclick="switch_display(this.parentNode, 'div')">hide/show</span>)
		<xsl:for-each select="//notes/note[position() &lt; 3]">
				<div class="item">
					<a href="{@href}"><xsl:copy-of select="* | text()"/>&#160; <span style="white-space:nowrap">
							<i><xsl:value-of select="authors"/><xsl:text> </xsl:text><xsl:value-of select="@year"/></i>
					</span></a>
				<!--<xsl:if test="position()=1">
					[<b style="color:green">new</b>]
				</xsl:if>-->
				</div>
		</xsl:for-each>
		</li>
	</ul>
	</div>
</div>
</xsl:template>

</xsl:stylesheet>


