<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
	<!--<xsl:param name="today" select="2"/>
	<xsl:param name="year" select="2016"/> <xsl:param name="offset" select="-1"/><xsl:param name="month_name" select="'March'"/><xsl:param name="days" select="31"/>-->
	
	<xsl:param name="datetime" select="''"/>
	<xsl:variable name="cdate">
		<xsl:choose>
			<xsl:when test="string-length($datetime) &gt; 8"><xsl:value-of select="$datetime"/></xsl:when>
			<xsl:otherwise><xsl:value-of select="current-date()"/></xsl:otherwise>
		</xsl:choose>
	</xsl:variable>
	<!--<xsl:variable name="cdate" select="current-date()"/>-->
	<xsl:variable name="year" select="number(substring(string($cdate), 0, 5))"/>
	<xsl:variable name="month" select="substring(string($cdate), 6, 2)"/>
	<xsl:variable name="today" select="substring(string($cdate), 9, 2)"/>
	
	<xsl:variable name="first_date_string" select="concat($year, '-', $month, '-01')"/>
	<xsl:variable name="first_date" select="xs:date($first_date_string)"/>
	
	
	<!-- modified from https://www.safaribooksonline.com/library/view/xslt-cookbook/0596003722/ch03s02.html-->
	<xsl:variable name="day_of_week">
		<xsl:variable name="day" select="substring-after(substring-after($first_date_string,'-'),'-')"/>
		<xsl:variable name="a" select="floor((14 - number($month)) div 12)"/>
		<xsl:variable name="y" select="$year - $a"/>
		<xsl:variable name="m" select="number($month) + 12 * $a - 2"/>
		<xsl:value-of select="(number($day) + $y + floor($y div 4) - floor($y div 100) 
			+ floor($y div 400) + floor((31 * $m) div 12)) mod 7"/>
	</xsl:variable>
	<xsl:param name="offset" select="(number($day_of_week) - 1) * -1"/>
	
	<!-- FIXME: fixed ? -->
	<xsl:variable name="days_string">
		<xsl:choose>
			<xsl:when test="number($month) = 1">31</xsl:when>
			<xsl:when test="number($month) = 2">
				<xsl:choose>
					<xsl:when test="$year=2016">29</xsl:when>
					<xsl:when test="($year - 2016) mod 4 = 0">29</xsl:when>
					<xsl:otherwise>28</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:when test="number($month) = 3">31</xsl:when>
			<xsl:when test="number($month) = 4">30</xsl:when>
			<xsl:when test="number($month) = 5">31</xsl:when>
			<xsl:when test="number($month) = 6">30</xsl:when>
			<xsl:when test="number($month) = 7">31</xsl:when>
			<xsl:when test="number($month) = 8">31</xsl:when>
			<xsl:when test="number($month) = 9">30</xsl:when>
			<xsl:when test="number($month) = 10">31</xsl:when>
			<xsl:when test="number($month) = 11">30</xsl:when>
			<xsl:when test="number($month) = 12">31</xsl:when>
		</xsl:choose>		
	</xsl:variable>
	<xsl:variable name="days" select="number($days_string)"/>
	
	<xsl:variable name="month_name">
		<xsl:choose>
			<xsl:when test="number($month) = 1">January</xsl:when>
			<xsl:when test="number($month) = 2">February</xsl:when>
			<xsl:when test="number($month) = 3">March</xsl:when>
			<xsl:when test="number($month) = 4">April</xsl:when>
			<xsl:when test="number($month) = 5">May</xsl:when>
			<xsl:when test="number($month) = 6">June</xsl:when>
			<xsl:when test="number($month) = 7">July</xsl:when>
			<xsl:when test="number($month) = 8">August</xsl:when>
			<xsl:when test="number($month) = 9">September</xsl:when>
			<xsl:when test="number($month) = 10">October</xsl:when>
			<xsl:when test="number($month) = 11">November</xsl:when>
			<xsl:when test="number($month) = 12">December</xsl:when>
		</xsl:choose>
	</xsl:variable>
	
	
	<xsl:variable name="style_td" select="'text-align:center;vertical-align:middle;height:3ex;width:88px'"/>
	<xsl:variable name="style_cell" select="'background-color:#DDDDDD'"/>
	
	<xsl:template match="/">
	
	<html>
		<head>
		  <!-- FIXME: style -->
		</head>
	
		<body style="max-width:640px">
	
				<table border="0" title="Implemented in XSLT 2.0 [{$cdate}]" style="color:#8B0000;">
					<tr>
				       		<td colspan="7" style="{$style_td};padding:0">
				       			<img  width="640" style="padding:0;margin:0" src="/static/calendar/cover2019_640.jpg"/>
				       		</td>
				       </tr>
				       <tr>
				       		<td colspan="7" style="padding-top:10px;padding-bottom:5px;font-weight:bold">
						<div>
						2019 mini-calendar (6.5" * 8.5") produced by Salicicola features parasitic plants of eastern Massachusetts. Available starting early January.

						</div> 
						<div style="padding-top:10px;padding-bottom:5px;">
						To order your calendar, write to webmaster@salicicola.com. 
						Please include your postal address. You will receive the calendar in the mail and then send the check. 
						The calendars are $10.00 (price includes shipping by first-class mail).  
						</div>
						</td>
				       </tr>
				       <!--<tr>
				       		<td colspan="7" style="{$style_td};padding:0">
				       			<img  width="640" style="padding:0;margin:0" src="/stati/calendar/cover2018_640B.jpg"/>
				       		</td>
				       </tr>-->
				       <!--
				       <tr>
				       		<th colspan="7" style="padding-top:2ex"><b><xsl:value-of select="$month_name"/><xsl:text> </xsl:text><xsl:value-of select="$year"/></b></th>
				       </tr>
				       <tr class="weekdays">
					  <th abbr="Sunday">Sun</th>
					  <th abbr="Monday">Mon</th>
					  <th abbr="Tuesday">Tue</th>
					  <th abbr="Wednesday">Wed</th>
					  <th abbr="Thursday">Thu</th>
					  <th abbr="Friday">Fri</th>
					  <th abbr="Saturday">Sat</th>
					</tr>
					<tr>
						<xsl:call-template name="cell">
							<xsl:with-param name="day" select="$offset"/>
						</xsl:call-template>
					</tr>
					<tr>
						<xsl:call-template name="cell">
							<xsl:with-param name="day" select="7 + $offset"/>
						</xsl:call-template>
					</tr>
					<tr>
						<xsl:call-template name="cell">
							<xsl:with-param name="day" select="14 + $offset"/>
						</xsl:call-template>
					</tr>
					<tr>
						<xsl:call-template name="cell">
							<xsl:with-param name="day" select="21 + $offset"/>
						</xsl:call-template>
					</tr>
					<tr>
						<xsl:call-template name="cell">
							<xsl:with-param name="day" select="28 + $offset"/>
						</xsl:call-template>
					</tr>
					<xsl:if test="28 + $offset + 6 &lt; $days">
					<tr title="{28 + $offset + 6}">
						<xsl:call-template name="cell">
							<xsl:with-param name="day" select="35 + $offset"/>
						</xsl:call-template>
					</tr>
					</xsl:if>
					-->
				</table>
			</body>
		</html>
	</xsl:template>
	
  <xsl:template name="row">
    <tr>
    	<xsl:call-template name="cell">
    	
    	</xsl:call-template>
    </tr>
    
  </xsl:template>

  <xsl:template name="cell">
  	<xsl:param name="day" select="1"/>
  	<xsl:param name="week_day" select="1"/>
  	<td style="{concat($style_td, ';', $style_cell)}">
  		<xsl:if test="$day = number($today)">
  			<xsl:attribute name="style" select="concat($style_td, ';background-color:yellow')"></xsl:attribute>
  		</xsl:if>
  		<xsl:if test="$day &gt; 0 and $day &lt;= $days">
  			<xsl:value-of select="$day"/>
  		</xsl:if>
  		<br/>
  	</td>
  	<xsl:if test="$week_day &lt; 7">
  		<xsl:call-template name="cell">
  			<xsl:with-param name="week_day" select="$week_day + 1"/>
  			<xsl:with-param name="day" select="$day + 1"/>
  		</xsl:call-template>
  	</xsl:if>
  </xsl:template>

</xsl:stylesheet>
