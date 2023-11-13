module.exports = {
	globDirectory: '/home/azfar/Workout-Log',
	globPatterns: [
	  '**/*.{py,json,md,pyc,db,html,js,png,css}'
	],
	swDest: '/home/azfar/Workout-Log/sw.js',
	ignoreURLParametersMatching: [
	  /^utm_/,
	  /^fbclid$/
	],
	runtimeCaching: [{
	  urlPattern: /\.(?:png|json|html|js|css)$/,
	  handler: 'CacheFirst',
	  options: {
		cacheName: 'my-cache', // Define a cache name for these files
		expiration: {
		  maxEntries: 50, // Maximum number of entries in the cache
		  maxAgeSeconds: 60 * 60 * 24 * 30 // Cache for 30 days (adjust as needed)
		}
	  }
	}]
  };