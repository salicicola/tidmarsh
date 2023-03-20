<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
   <xsl:output method="xml" indent="no" omit-xml-declaration="yes" />
   <xsl:template name="checklists">
   <div id="checklists">
        <xsl:if test="not ($page='checklists')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div style="float:right;margin-left:10px;">
		<img align="right" alt="" title="" width="300" border="1" onclick="openImage(this)" 
		src="/static/photos/201508/20150821olymp5786a.jpg"/>
	</div>	
	<div class="header"><h2>Checklists</h2></div>	
	<xsl:for-each select="/*/checklists/*">
		<div class="section">
			<div class="section_header">
				<xsl:choose>
					<xsl:when test="@href">
						<a href="{@href}"><xsl:value-of select="@title"/></a> <!-- XXX -->
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="@title"/>
					</xsl:otherwise>
				</xsl:choose>
			</div>
			<xsl:choose>
				<xsl:when test="page">
					<xsl:for-each select="page">
						<div class="item">
							<a href="{@href}"> <!-- XXX -->
							<xsl:value-of select="@title"/>
							<xsl:copy-of select="* | text()"/>
							</a>
						</div>
					</xsl:for-each>
				</xsl:when>
			<xsl:otherwise>
				<div class="item"><br/></div>
			</xsl:otherwise>
			</xsl:choose>		
		</div>		
	</xsl:for-each>
</div>
</xsl:template>

</xsl:stylesheet>
