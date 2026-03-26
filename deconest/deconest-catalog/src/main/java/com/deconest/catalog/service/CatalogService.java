package com.deconest.catalog.service;

import com.deconest.catalog.api.dto.CategoryResponse;
import com.deconest.catalog.api.dto.CreateCategoryRequest;
import com.deconest.catalog.api.dto.CreateProductRequest;
import com.deconest.catalog.api.dto.CreateSubcategoryRequest;
import com.deconest.catalog.api.dto.ProductResponse;
import com.deconest.catalog.api.dto.SubcategoryResponse;
import com.deconest.catalog.domain.Category;
import com.deconest.catalog.domain.Product;
import com.deconest.catalog.domain.ProductStatus;
import com.deconest.catalog.domain.Subcategory;
import com.deconest.catalog.repository.CategoryRepository;
import com.deconest.catalog.repository.ProductRepository;
import com.deconest.catalog.repository.SubcategoryRepository;
import com.deconest.user.domain.UserAccount;
import com.deconest.user.repository.UserAccountRepository;
import jakarta.persistence.EntityNotFoundException;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class CatalogService {

    private final CategoryRepository categoryRepository;
    private final SubcategoryRepository subcategoryRepository;
    private final ProductRepository productRepository;
    private final UserAccountRepository userAccountRepository;

    public CatalogService(
            CategoryRepository categoryRepository,
            SubcategoryRepository subcategoryRepository,
            ProductRepository productRepository,
            UserAccountRepository userAccountRepository) {
        this.categoryRepository = categoryRepository;
        this.subcategoryRepository = subcategoryRepository;
        this.productRepository = productRepository;
        this.userAccountRepository = userAccountRepository;
    }

    public CategoryResponse createCategory(CreateCategoryRequest request) {
        Category category = new Category(
                request.name(),
                request.description(),
                request.imageUrl(),
                request.availableForSale(),
                request.availableForRent());
        return toCategoryResponse(categoryRepository.save(category));
    }

    @Transactional(readOnly = true)
    public List<CategoryResponse> listCategories() {
        return categoryRepository.findAll().stream()
                .map(this::toCategoryResponse)
                .toList();
    }

    public SubcategoryResponse createSubcategory(CreateSubcategoryRequest request) {
        Category category = categoryRepository.findById(request.categoryId())
                .orElseThrow(() -> new EntityNotFoundException("Category not found: " + request.categoryId()));

        Subcategory subcategory = new Subcategory(category, request.name(), request.description());
        return toSubcategoryResponse(subcategoryRepository.save(subcategory));
    }

    @Transactional(readOnly = true)
    public List<SubcategoryResponse> listSubcategories(Long categoryId) {
        List<Subcategory> subcategories = categoryId == null
                ? subcategoryRepository.findAll()
                : subcategoryRepository.findByCategoryId(categoryId);
        return subcategories.stream()
                .map(this::toSubcategoryResponse)
                .toList();
    }

    public ProductResponse createProduct(CreateProductRequest request) {
        UserAccount seller = userAccountRepository.findById(request.sellerId())
                .orElseThrow(() -> new EntityNotFoundException("Seller not found: " + request.sellerId()));
        Category category = categoryRepository.findById(request.categoryId())
                .orElseThrow(() -> new EntityNotFoundException("Category not found: " + request.categoryId()));
        Subcategory subcategory = subcategoryRepository.findById(request.subcategoryId())
                .orElseThrow(() -> new EntityNotFoundException("Subcategory not found: " + request.subcategoryId()));

        Product product = new Product(
                seller,
                category,
                subcategory,
                request.brandName(),
                request.name(),
                request.productDescription(),
                request.materialDescription(),
                request.price(),
                request.quantity(),
                request.imageUrl1(),
                request.imageUrl2(),
                request.imageUrl3(),
                request.imageUrl4(),
                request.measurements(),
                request.maintenanceNotes(),
                request.color(),
                request.status() == null ? ProductStatus.DRAFT : request.status());

        return toProductResponse(productRepository.save(product));
    }

    @Transactional(readOnly = true)
    public List<ProductResponse> listProducts(Long sellerId, Long categoryId, ProductStatus status) {
        List<Product> products;
        if (sellerId != null) {
            products = productRepository.findBySellerId(sellerId);
        } else if (categoryId != null) {
            products = productRepository.findByCategoryId(categoryId);
        } else if (status != null) {
            products = productRepository.findByStatus(status);
        } else {
            products = productRepository.findAll();
        }

        return products.stream()
                .map(this::toProductResponse)
                .toList();
    }

    private CategoryResponse toCategoryResponse(Category category) {
        return new CategoryResponse(
                category.getId(),
                category.getName(),
                category.getDescription(),
                category.getImageUrl(),
                category.isEnabled(),
                category.isAvailableForSale(),
                category.isAvailableForRent());
    }

    private SubcategoryResponse toSubcategoryResponse(Subcategory subcategory) {
        return new SubcategoryResponse(
                subcategory.getId(),
                subcategory.getCategory().getId(),
                subcategory.getName(),
                subcategory.getDescription(),
                subcategory.isEnabled());
    }

    private ProductResponse toProductResponse(Product product) {
        return new ProductResponse(
                product.getId(),
                product.getSeller().getId(),
                product.getCategory().getId(),
                product.getSubcategory().getId(),
                product.getBrandName(),
                product.getName(),
                product.getProductDescription(),
                product.getMaterialDescription(),
                product.getPrice(),
                product.getQuantity(),
                product.getImageUrl1(),
                product.getImageUrl2(),
                product.getImageUrl3(),
                product.getImageUrl4(),
                product.getMeasurements(),
                product.getMaintenanceNotes(),
                product.getColor(),
                product.getStatus());
    }
}

