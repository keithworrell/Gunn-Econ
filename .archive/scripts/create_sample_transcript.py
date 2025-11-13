#!/usr/bin/env python3
"""
Creates a sample economics transcript PDF for testing the pipeline
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

OUTPUT_FILE = "economics-spanish/original-transcripts/video-01-supply-and-demand.pdf"

# Sample economics transcript content
TRANSCRIPT_CONTENT = """
SUPPLY AND DEMAND

Introduction to Economic Principles

In economics, supply and demand is a fundamental concept that describes the relationship between the availability of a product and the desire for that product. This relationship determines the price of goods in a market economy.

The Law of Demand

The law of demand states that, all else being equal, as the price of a product increases, the quantity demanded decreases. Conversely, as the price decreases, the quantity demanded increases. This inverse relationship creates the downward-sloping demand curve.

For example, if the price of coffee increases from three dollars to five dollars per cup, fewer consumers will be willing to purchase coffee at the higher price. Some may switch to tea, others may reduce their consumption, and some may stop buying coffee altogether.

The Law of Supply

The law of supply states that, all else being equal, an increase in price results in an increase in quantity supplied. As prices rise, producers are motivated to produce more because they can achieve higher profits. The supply curve slopes upward, showing this direct relationship between price and quantity supplied.

Using our coffee example, if coffee shops can sell coffee at five dollars per cup instead of three dollars, they have a greater incentive to produce and sell more coffee. Higher prices make it profitable for suppliers to expand production.

Market Equilibrium

The point where supply and demand curves intersect is called the market equilibrium. At this price point, the quantity that consumers want to buy equals the quantity that producers want to sell. There is no shortage or surplus.

When markets are not in equilibrium, there are forces that push them toward equilibrium. If the price is too high, there will be a surplus, and sellers will lower prices to sell excess inventory. If the price is too low, there will be a shortage, and prices will rise as consumers compete for limited supply.

Factors Affecting Demand

Several factors can shift the demand curve:

Consumer income: When people have more money, they tend to buy more goods. Normal goods see increased demand when income rises, while inferior goods may see decreased demand.

Consumer preferences: Changes in taste, fashion, or social trends can increase or decrease demand for specific products.

Prices of related goods: The demand for a product can be affected by the prices of substitute goods or complementary goods. For example, if the price of tea increases, the demand for coffee might increase as consumers switch beverages.

Expectations: If consumers expect prices to rise in the future, they may increase current demand. Similarly, expectations of future income changes can affect present consumption.

Number of buyers: An increase in the number of potential consumers in a market will shift the demand curve to the right.

Factors Affecting Supply

Supply can also be shifted by various factors:

Input costs: If the cost of resources needed for production increases, the supply curve shifts to the left, meaning less is supplied at each price point.

Technology: Improvements in technology can make production more efficient, shifting the supply curve to the right.

Number of sellers: More competition typically means more supply in the market.

Expectations: If producers expect prices to rise in the future, they might hold back current supply to sell later at higher prices.

Government policies: Taxes, subsidies, and regulations can all affect production costs and therefore supply.

Price Elasticity

Price elasticity measures how responsive quantity demanded or supplied is to price changes. Some goods are highly elastic, meaning small price changes lead to large changes in quantity. Other goods are inelastic, where quantity changes little despite significant price changes.

Necessities like basic food items and medications tend to be inelastic because people need them regardless of price. Luxury goods and items with many substitutes tend to be more elastic.

Real-World Applications

Understanding supply and demand helps explain many real-world phenomena. Housing prices in desirable cities rise because demand is high and supply is limited. Agricultural prices fluctuate with weather conditions that affect supply. Technology prices often fall over time as production becomes more efficient and supply increases.

Businesses use supply and demand analysis to make pricing decisions. Governments consider these principles when creating policies on minimum wages, rent control, and taxation. Investors analyze supply and demand in various markets to make investment decisions.

Conclusion

Supply and demand forms the foundation of market economics. These forces interact constantly in free markets to determine prices and allocate resources. While the basic model is simplified, it provides powerful insights into economic behavior and helps us understand the complex dynamics of modern economies.

The next video will explore how government intervention affects market outcomes and the concept of market efficiency.
"""

def create_sample_pdf():
    """Create a sample PDF transcript"""
    print("Creating sample economics transcript PDF...")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Create PDF
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#000000',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#000000',
        spaceAfter=12,
        spaceBefore=18,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor='#000000',
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica'
    )

    # Build content
    story = []

    # Parse content into sections
    lines = TRANSCRIPT_CONTENT.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue

        # Determine if it's a title/heading
        if line.isupper() and len(line) < 50:
            story.append(Paragraph(line, title_style))
        elif line and not line[0].islower() and len(line) < 100 and line.count(' ') < 6:
            story.append(Paragraph(line, heading_style))
        else:
            story.append(Paragraph(line, body_style))

    # Build PDF
    doc.build(story)
    print(f"✓ Sample transcript created: {OUTPUT_FILE}")
    print(f"  File size: {os.path.getsize(OUTPUT_FILE)} bytes")

if __name__ == "__main__":
    create_sample_pdf()
