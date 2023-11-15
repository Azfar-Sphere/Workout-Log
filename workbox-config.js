module.exports = {
	globDirectory: 'webapp/',
	globPatterns: [
		'**/*.{py,pyc,db,html,js,png,css,pdf,doc,docx,txt}'
	],
	swDest: 'webapp/sw.js',
	ignoreURLParametersMatching: [
		/^utm_/,
		/^fbclid$/
	]
};