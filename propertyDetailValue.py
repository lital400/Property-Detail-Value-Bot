from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import csv

my_data = np.genfromtxt('Properties.csv', dtype=str, delimiter=',', skip_header=1)

my_file = csv.writer(open('propertyDetailValue.csv', 'w', newline=''))
my_file.writerow(['Constituent ID', 'Real Estate Number', 'Tax District', 'Property Use', 'Subdivision', 'Total Area', 'Total Building Value', 'Extra Feature Value', 'Land Value (Market)', 'Land Value (Agric.)', 'Just (Market) Value', 'Assessed Value', 'Cap Diff/Portability Amt', 'Exemptions', 'Taxable Value'])

for i, row in enumerate(my_data):
    rowValue = [row[0], row[1]]     # add Constituent ID + Real Estate Number

    if row[2] == 'n/a':             # if no RE# provided
        my_file.writerow(rowValue)
        continue
    else:                           # if RE# is provided
        browser = webdriver.Chrome('C:/WebDriver/bin/chromedriver')
        browser.get("https://paopropertysearch.coj.net/Basic/Search.aspx")

        re1_search_input = browser.find_element_by_id('ctl00_cphBody_tbRE6')
        re1_search_input.send_keys(row[2])       # row[2] = RE1
        re2_search_input = browser.find_element_by_id('ctl00_cphBody_tbRE4')
        re2_search_input.send_keys(row[3])       # row[3] = RE2


        search_button = browser.find_element_by_id('ctl00_cphBody_bSearch')
        search_button.click()

        try:
            text = "Detail.aspx"
            property_link = browser.find_element_by_xpath('//a[contains(@href, "%s")]' % text)
            property_link.click()
        except NoSuchElementException:
            browser.close()
            my_file.writerow(rowValue)
            continue

        taxDistrict = browser.find_element_by_id('ctl00_cphBody_lblTaxDistrict')
        rowValue.append(taxDistrict.text)

        propertyUse = browser.find_element_by_id('ctl00_cphBody_lblPropertyUse')
        rowValue.append(propertyUse.text)

        subdivision = browser.find_element_by_id('ctl00_cphBody_lblSubdivision')
        rowValue.append(subdivision.text)

        totalArea = browser.find_element_by_id('ctl00_cphBody_lblTotalArea1')
        rowValue.append(totalArea.text)

        totalBldVal = browser.find_element_by_id('ctl00_cphBody_lblBuildingValueCertified')
        rowValue.append(totalBldVal.text)

        extraFeature = browser.find_element_by_id('ctl00_cphBody_lblExtraFeatureValueCertified')
        rowValue.append(extraFeature.text)

        landValMarket = browser.find_element_by_id('ctl00_cphBody_lblLandValueMarketCertified')
        rowValue.append(landValMarket.text)

        landValAgr = browser.find_element_by_id('ctl00_cphBody_lblLandValueAgricultureCertified')
        rowValue.append(landValAgr.text)

        justMarketVal = browser.find_element_by_id('ctl00_cphBody_lblJustMarketValueCertified')
        rowValue.append(justMarketVal.text)

        assessedValue = browser.find_element_by_id('ctl00_cphBody_lblAssessedValueA10Certified')
        rowValue.append(assessedValue.text)

        capDiff = browser.find_element_by_id('ctl00_cphBody_lblCapDiffCertified')
        rowValue.append(capDiff.text)

        exemptions = browser.find_element_by_id('ctl00_cphBody_lblExemptValueCertified')
        rowValue.append(exemptions.text)

        taxableValue = browser.find_element_by_id('ctl00_cphBody_lblTaxableValueCertified')
        rowValue.append(taxableValue.text)

        browser.close()
        my_file.writerow(rowValue)

my_file.close()
