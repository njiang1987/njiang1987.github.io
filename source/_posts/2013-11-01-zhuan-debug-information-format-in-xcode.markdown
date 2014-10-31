---
layout: post
title: '[转]Debug Information Format in Xcode'
categories:
- 未分类
tags: []
published: true
comments: true
---
<p><section>
<h3>DEBUG_INFORMATION_FORMAT (Debug Information Format)</h3>
<a name="//apple_ref/doc/uid/TP40003931-CH3-DontLinkElementID_42"></a><a name="//apple_ref/doc/uid/TP40003931-CH3-DontLinkElementID_43"></a>
<div>
<table border="0" cellspacing="0" cellpadding="5">
<tbody>
<tr>
<td scope="row">Description:</td>
<td>Identifier. Identifies the format used to store the binary’s debug information.</td>
</tr>
<tr>
<td scope="row">Values:</td>
<td>
<ul>
	<li><code>stabs</code>: Use the Stabs format and place the debug information in the binary.</li>
	<li><code>dwarf</code>: Use the DWARF format and place the debug information in the binary.</li>
	<li><code>dwarf-with-dsym</code>: Use the DWARF format and place the debug information in a dSYM file.</li>
</ul>
</td>
</tr>
<tr>
<td scope="row">Default value:</td>
<td><code>dwarf</code></td>
</tr>
<tr>
<td scope="row">Prerequisite for:</td>
<td><a href="https://developer.apple.com/library/mac/documentation/DeveloperTools/Reference/XcodeBuildSettingRef/1-Build_Setting_Reference/build_setting_ref.html#//apple_ref/doc/uid/TP40003931-CH3-SW7">“GCC_ENABLE_SYMBOL_SEPARATION (Separate PCH Symbols).”</a></td>
</tr>
</tbody>
</table>
</div>
</section><section><a title="DEPLOYMENT_POSTPROCESSING (Deployment Postprocessing)" name="//apple_ref/doc/uid/TP40003931-CH3-SW53"></a><a title="DEPLOYMENT_POSTPROCESSING (Deployment Postprocessing)" name="//apple_ref/doc/uid/TP40003931-CH3-SW53"></a><section>
<h3>GCC_ENABLE_SYMBOL_SEPARATION (Separate PCH Symbols)</h3>
<a name="//apple_ref/doc/uid/TP40003931-CH3-DontLinkElementID_120"></a><a name="//apple_ref/doc/uid/TP40003931-CH3-DontLinkElementID_121"></a>
<div>
<table border="0" cellspacing="0" cellpadding="5">
<tbody>
<tr>
<td scope="row">Description:</td>
<td>Boolean value. Specifies whether the compiler generates a separate file containing the debug symbols when compiling a precompiled (prefix) header (PCH). A separate file with debug symbols can improve build time.</td>
</tr>
<tr>
<td scope="row">Prerequisite:</td>
<td><code>$DEBUG_INFORMATION_FORMAT = stabs AND $GCC_DEBUGGING_SYMBOLS = full</code></td>
</tr>
<tr>
<td scope="row">Values:</td>
<td>
<ul>
	<li><code>YES</code>: Generates separate file containing debug symbols for a precompiled header.</li>
	<li><code>NO</code>: Does not generate separate debug symbol file.</li>
</ul>
</td>
</tr>
<tr>
<td scope="row">Default value:</td>
<td>
<ul>
	<li><code>YES</code>: When <code>$MACH_O_TYPE != staticlib</code>.</li>
	<li><code>NO</code>: Is the alternative.</li>
</ul>
</td>
</tr>
<tr>
<td scope="row">Effector:</td>
<td><a href="https://developer.apple.com/library/mac/documentation/DeveloperTools/Reference/XcodeBuildSettingRef/1-Build_Setting_Reference/build_setting_ref.html#//apple_ref/doc/uid/TP40003931-CH3-SW73">“MACH_O_TYPE”</a></td>
</tr>
<tr>
<td scope="row">Companions:</td>
<td><a href="https://developer.apple.com/library/mac/documentation/DeveloperTools/Reference/XcodeBuildSettingRef/1-Build_Setting_Reference/build_setting_ref.html#//apple_ref/doc/uid/TP40003931-CH3-SW52">“DEBUG_INFORMATION_FORMAT (Debug Information Format),”</a> <a href="https://developer.apple.com/library/mac/documentation/DeveloperTools/Reference/XcodeBuildSettingRef/1-Build_Setting_Reference/build_setting_ref.html#//apple_ref/doc/uid/TP40003931-CH3-SW8">“GCC_DEBUGGING_SYMBOLS (Level of Debug Symbols).”</a></td>
</tr>
</tbody>
</table>
</div>
</section><a title="DEPLOYMENT_POSTPROCESSING (Deployment Postprocessing)" name="//apple_ref/doc/uid/TP40003931-CH3-SW53"></a><a title="DEPLOYMENT_POSTPROCESSING (Deployment Postprocessing)" name="//apple_ref/doc/uid/TP40003931-CH3-SW53"></a><section><a title="GCC_FEEDBACK_DIRECTED_OPTIMIZATION (Feedback-Directed Optimization)" name="//apple_ref/doc/uid/TP40003931-CH3-SW117"></a></section></section></p>
