package main

import (
	"log"
	"os"

	"github.com/financial-rag/backend-go/handlers"
	"github.com/financial-rag/backend-go/middleware"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

func main() {
	// Load environment variables
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found, using system environment variables")
	}

	// Get configuration from environment
	port := os.Getenv("GO_PORT")
	if port == "" {
		port = "8080"
	}

	env := os.Getenv("GO_ENV")
	if env == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	// Initialize Gin router
	router := gin.Default()

	// Apply middleware
	router.Use(middleware.CORSMiddleware())

	// Health check endpoint
	router.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status": "healthy",
			"service": "backend-go",
		})
	})

	// API routes
	api := router.Group("/api")
	{
		api.POST("/query", handlers.HandleQuery)
	}

	// Start server
	log.Printf("Starting server on port %s", port)
	if err := router.Run(":" + port); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
