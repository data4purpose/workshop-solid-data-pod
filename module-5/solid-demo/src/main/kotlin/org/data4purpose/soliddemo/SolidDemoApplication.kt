package org.data4purpose.soliddemo

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class SolidDemoApplication

fun main(args: Array<String>) {
    runApplication<SolidDemoApplication>(*args)
}
