package middleware

import (
	"os"
	"strings"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

// CORSMiddleware configures CORS for the API
func CORSMiddleware() gin.HandlerFunc {
	config := cors.DefaultConfig()

	// Get allowed origins from environment variable
	allowedOrigins := os.Getenv("ALLOWED_ORIGINS")

	if allowedOrigins != "" {
		// Split comma-separated origins from environment
		config.AllowOrigins = strings.Split(allowedOrigins, ",")
	} else {
		// Default origins for development
		config.AllowOrigins = []string{
			"http://localhost:3000",
			"http://frontend:3000",
			"https://*.vercel.app",
		}
	}

	config.AllowMethods = []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"}
	config.AllowHeaders = []string{"Origin", "Content-Type", "Accept", "Authorization"}
	config.AllowCredentials = true

	return cors.New(config)
}
