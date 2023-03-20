<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:template name="style">
		<style type="text/css">
		body {
			margin: 0;
			padding: 0;
			background-color:<xsl:value-of select="$bgcolor"/>;
		}
		#wrapper {
			width: 1004px;   /* 972px; */
			margin: 0 auto;
			color:<xsl:value-of select="$color"/>; 
			background-color: <xsl:value-of select="$bgcolor"/>;
		}
		#header {
			height:72px;
			background-color: <xsl:value-of select="$bgcolor"/>;
			margin-bottom:3px;
			white-space:nowrap;
		}
		#sidebar {
			width: 325px; /* 305px; */
			background-color:<xsl:value-of select="$bgcolor"/>;
			float:left;
			margin-right:3px;
			white-space:nowrap;
		}
		#sidebar h2 {
			padding-left:5px;
			margin-bottom:0;
			margin-top:14px;
		}	
		#content {
			width:672px;  /* 658px; */
			background-color:<xsl:value-of select="$bgcolor"/>;
			padding-left:3px;
			float:left;
			padding-top:14px;
		}
		#footer {
			clear:both;
			background-color:<xsl:value-of select="$bgcolor"/>;
			height: 4ex;
		}
		a {
			color: <xsl:value-of select="$color"/>; 
			background-color: transparent;
			text-decoration: none;
		}		
		a:link {
			color: <xsl:value-of select="$color"/>;
			background-color: transparent;
			text-decoration: none;
		}
		a:visited {
			color: <xsl:value-of select="$color"/>; 
			background-color: transparent;
			text-decoration:none;
		}
		a:active {
			color: #ff0000; 
			background-color: transparent;
			text-decoration:none;
		}
		a:hover {
			color: #ff0000; 
			background-color: transparent;
			text-decoration:none;
		}
		
		
div.header, div.section, div.items {
	margin-left:1em;margin-right:5px;
}
div.section_header {
	font-weight:bold;
}
div.header h2 {
margin-top:0;padding-top:0;margin-bottom:0;padding-bottom:0.5ex;
}

/* div.items { */
/* margin-left:1em;margin-right:5px; */
/* } */

div.item {
	text-indent:-2ex;padding-left:4ex;padding-bottom:0.4ex;
}

div.item_compact {
	text-indent:-2ex;padding-left:4ex;padding-bottom:0.1ex;
}

		</style>
	</xsl:template>
</xsl:stylesheet>
