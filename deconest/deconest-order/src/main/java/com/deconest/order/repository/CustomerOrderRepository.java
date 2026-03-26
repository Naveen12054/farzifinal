package com.deconest.order.repository;

import com.deconest.order.domain.CustomerOrder;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CustomerOrderRepository extends JpaRepository<CustomerOrder, Long> {

    List<CustomerOrder> findByCustomerEmailOrderByCreatedAtDesc(String email);

    Optional<CustomerOrder> findByIdAndCustomerEmail(Long id, String email);
}
