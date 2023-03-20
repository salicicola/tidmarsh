<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />
	<xsl:variable name="years" select="tokenize(//quiz/years, ' ')"/>
	<xsl:variable name="years_stat" select="tokenize(//quiz/years_stat, ' ')"/>
	<xsl:template name="quiz">
		<div id="quiz">
			<xsl:if test="not ($page='quiz')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
			<div style="float:right;margin-left:10px;">
				<img align="right" alt="" title="" width="300" border="1"  src="{//quiz/image_top/@src}"/>
				<br clear='all'/>
				<img width="300" border="1" align="right" style="margin-top:5px;margin-bottom:3px"
					src="{//quiz/image_bottom/@src}" title="" alt=""/> 
			</div>

			<div style="margin-left:1em;margin-right:5px">
				<h2 style="margin-top:0;padding-top:0;margin-bottom:0;padding-bottom:1ex;">
					<!--<a style="font-weight:bold" href="http://salicicola.com/photos/plants/quiz/{$years[last()]}">-->April Fool's Day Quizzes
					
						<!--<xsl:value-of select="$years[last()]"/></a>-->
				</h2>
				<div style="text-indent:-2ex;padding-left:4ex"><br/></div>
			</div>
			
			<div style="margin-left:1em;margin-right:5px"> 
				<b>Choose from 14 quizzes!</b> <!--<xsl:value-of select="$years[1]"/>&#8211;<xsl:value-of select="number($years[last()])"/></b>--><!-- -1 -->
				<div style="padding-left:3ex;margin-top:0.5ex">
					<xsl:for-each select="$years[position()]"><!--  != last()-->
						<xsl:sort order="ascending" data-type="number"/>
							[<a style="text-decoration: underline" href="http://salicicola.com/photos/plants/quiz/{.}" target="_blank"><xsl:value-of select="position()"/></a>] 
							<xsl:if test="not (number(position()) mod 5)"><br/></xsl:if>
					</xsl:for-each>		
				</div>
			</div>

			<div style="margin-left:1em;margin-right:5px;margin-top:1.5ex;"> 
				<b>Results (Statistics)</b>
				<div style="padding-left:3ex;margin-top:0.5ex">
					[<a href="http://salicicola.com/quiz/2019/stat"><xsl:value-of select="14"/></a>]
					[<a href="http://salicicola.com/quiz/2018/stat"><xsl:value-of select="13"/></a>]
					[<a href="http://salicicola.com/quiz/2017/stat"><xsl:value-of select="12"/></a>]
					[<a href="http://salicicola.com/quiz/2016/stat"><xsl:value-of select="11"/></a>]
					[<a href="http://salicicola.com/quiz/2015/stat"><xsl:value-of select="10"/></a>]
					[<a href="http://salicicola.com/quiz/2014/stat"><xsl:value-of  select="9"/></a>]
					<!--<xsl:for-each select="$years_stat[position() != last()]">
						<xsl:sort order="descending" data-type="number"/>
						[<a href="http://salicicola.com/quiz/{.}/stat"><xsl:value-of select="13 - position()"/></a>]
					</xsl:for-each>-->
				</div>
				<!--<div style="text-indent:-2ex;padding-left:4ex"><br/></div>-->
			</div>

			
			<img src="{//quiz/image_middle/@src}" width="300" vspace="3" align="left" 
				style="margin-top:4ex;margin-left:1em;padding-right:5px;"/>
		</div>
	</xsl:template>
</xsl:stylesheet>
