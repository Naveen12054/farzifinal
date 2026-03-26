package com.deconest.catalog.api;

import com.deconest.catalog.api.dto.CategoryResponse;
import com.deconest.catalog.api.dto.CreateCategoryRequest;
import com.deconest.catalog.api.dto.CreateProductRequest;
import com.deconest.catalog.api.dto.CreateSubcategoryRequest;
import com.deconest.catalog.api.dto.ProductResponse;
import com.deconest.catalog.api.dto.SubcategoryResponse;
import com.deconest.catalog.domain.ProductStatus;
import com.deconest.catalog.service.CatalogService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/catalog")
public class CatalogController {

    private final CatalogService catalogService;

    public CatalogController(CatalogService catalogService) {
        this.catalogService = catalogService;
    }

    @GetMapping("/categories")
    public List<CategoryResponse> listCategories() {
        return catalogService.listCategories();
    }

    @PostMapping("/categories")
    public CategoryResponse createCategory(@Valid @RequestBody CreateCategoryRequest request) {
        return catalogService.createCategory(request);
    }

    @GetMapping("/subcategories")
    public List<SubcategoryResponse> listSubcategories(@RequestParam(required = false) Long categoryId) {
        return catalogService.listSubcategories(categoryId);
    }

    @PostMapping("/subcategories")
    public SubcategoryResponse createSubcategory(@Valid @RequestBody CreateSubcategoryRequest request) {
        return catalogService.createSubcategory(request);
    }

    @GetMapping("/products")
    public List<ProductResponse> listProducts(
            @RequestParam(required = false) Long sellerId,
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) ProductStatus status) {
        return catalogService.listProducts(sellerId, categoryId, status);
    }

    @PostMapping("/products")
    public ProductResponse createProduct(@Valid @RequestBody CreateProductRequest request) {
        return catalogService.createProduct(request);
    }
}
