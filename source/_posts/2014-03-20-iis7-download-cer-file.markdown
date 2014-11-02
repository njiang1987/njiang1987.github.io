---
layout: post
title: IIS7 download cer file
categories:
- 技术
tags: [Other]
published: true
comments: true
---
<p>To add a file type CER IIS7 and allow it to download, you have to make these changes:
<ol>
	<li>Add MIME type: .cer - application/x-x509-ca-cert</li>
	<li>Remove Handler Mappings: SecurityCertificate *.cer</li>
</ol></p>
