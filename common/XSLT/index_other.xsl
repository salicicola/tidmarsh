<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />

<xsl:template name="other">
   <div id="other">
        <xsl:if test="not ($page='other')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div style="float:right;margin-left:10px;">
		<img alt="" title="bullfrog" onclick="openImage(this)"
                                src="/static/images/index_animals4771.jpg" align="right" border="1" width="280" style="margin-bottom:2px;"/><br/>
			<img alt="" title="mallard duck" onclick="openImage(this)" 
				src="/static/photos/200804/20080430kodak0088cs.jpg" align="right" border="1" height="180" style="margin-bottom:2px"/><br/> 
			<img alt="" title="bumblebee robber fly" onclick="openImage(this)" 
				src="/static/images/Fly_Image.jpeg" align="right" border="1" width="280" style="margin-bottom:2px;"/>
		</div>
<xsl:call-template name="animals"/>
		<div  class="section">
			 <!-- /20080430kodak0088cs.jpg /animals_below.jpg 656 -->
		</div>
</div>
</xsl:template>
</xsl:stylesheet>
