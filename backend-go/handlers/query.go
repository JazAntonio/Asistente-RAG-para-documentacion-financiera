package handlers

import (
	"log"
	"net/http"
	"strings"

	"github.com/financial-rag/backend-go/clients"
	"github.com/gin-gonic/gin"
)

// QueryRequest represents the incoming query request
type QueryRequest struct {
	Query string `json:"query" binding:"required"`
}

var ragClient = clients.NewRAGClient()

// HandleQuery processes user queries and returns RAG responses
func HandleQuery(c *gin.Context) {
	var req QueryRequest

	// Validate request body
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid request format",
			"details": err.Error(),
		})
		return
	}

	// Validate query content
	query := strings.TrimSpace(req.Query)
	if query == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Query cannot be empty",
		})
		return
	}

	// Enforce query length limits (security measure)
	if len(query) > 1000 {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Query too long (max 1000 characters)",
		})
		return
	}

	// Call RAG service
	log.Printf("Processing query: %s", query)
	response, err := ragClient.Query(query)
	if err != nil {
		log.Printf("RAG service error: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Failed to process query",
			"details": err.Error(),
		})
		return
	}

	// Return successful response
	c.JSON(http.StatusOK, response)
}
