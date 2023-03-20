<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:param name="text" select="''"/>
	<xsl:template match="/">
			<xsl:for-each select="/*/*[contains(., $text)]">
				<li onclick="document.getElementById('plantname').value = this.innerHTML; document.getElementById('pnids').value=this.id;this.parentElement.style.display='none'" 
					title="{authors}" id="{PNID}"><xsl:value-of select="latname"/></li>
			</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
