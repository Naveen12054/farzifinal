package com.deconest.catalog.repository;

import com.deconest.catalog.domain.Subcategory;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SubcategoryRepository extends JpaRepository<Subcategory, Long> {

    List<Subcategory> findByCategoryId(Long categoryId);
}

